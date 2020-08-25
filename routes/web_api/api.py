from flask import Blueprint,render_template,request
from application.utilities.util import required_params
from application.models.tasks import Task
from application.models.users import User
from application.utilities.flask import APIError,APIResponse
from application.utilities.token_verification import verify_token
from http import HTTPStatus
from application.routes.web_api import consumer_web_api_check

dash_bp = Blueprint("dashboard",__name__,template_folder="templates")
        
@dash_bp.route('/',methods=['GET'])
def home():
    return "Welcome"

@dash_bp.route('/create_user',methods=['POST'])
@required_params(['token'])
def create_user(token):
    data = verify_token(token)
    if data:
        name = data['name']
        email = data['upn']
        user = User.get_by_email(email)
        if user:
            return APIResponse(message="Login successful", data={
                'access_token': User.generate_access_token(user)
            }, status=HTTPStatus.OK)

        else:
            user = User(name,email)
            user.save()
            return APIResponse(message="Registration successful", data={
                'access_token': User.generate_access_token(user)
            }, status=HTTPStatus.OK)
    else:
        return APIError(message='Invalid Token', status= HTTPStatus.UNAUTHORIZED)


@dash_bp.route('/add_task',methods=['POST'])
@required_params(['name','description','url'])
@consumer_web_api_check
def add_task(name,description,url):
    user = request.data["auth_user"]
    task = Task(name,user.id,description,url)
    task.save()
    return APIResponse(message="Task Created",status=HTTPStatus.OK)

@dash_bp.route('/get_task', methods=['POST'])
@required_params(['id'])
@consumer_web_api_check
def get_task(id):
    task = Task.get(id)
    response_data = {'name': task.name, 'created_by': task.created_by , 'created_on': task.created_on , 'status': 'completed' if Task.end_on else 'in progress'}
    return APIResponse(message="Task Returned", data=response_data, status=HTTPStatus.OK)

@dash_bp.route('/get_all', methods=['POST'])
@required_params(['selected_date'])
@consumer_web_api_check
def get_all(selected_date):
    user = request.data["auth_user"]
    if user.task:
        task_list = user.task
        data = []
        for task in task_list:
            if str(task.created_on.date()) == selected_date:
                data.append({'name': task.name, 'created_on': str(task.created_on.date()),'created_time': str(task.created_on.time()),'created_weekday': task.created_on.weekday() , 'description': task.description,'url': task.url,'end_on': str(task.end_on.date()) if task.end_on else None,'end_time': str(task.end_on.time()) if task.end_on else None,'end_weekday': task.end_on.weekday() if task.end_on else None ,'status': 'completed' if task.end_on else 'in progress', 'id': task.id})
        return APIResponse(message="Task Returned", data={'data': data,'length': len(data)}, status=HTTPStatus.OK)
    return APIError(message='No Task Found', status= HTTPStatus.NOT_FOUND)

@dash_bp.route('/end_task', methods=['POST'])
@required_params(['task_id'])
@consumer_web_api_check
def end_task(task_id):
    user = request.data["auth_user"]
    task_list = user.task
    for task in task_list:
        if task.id == task_id:
            task.end_now()
    return APIResponse(message='Task Ended',status=HTTPStatus.OK)

@dash_bp.route('/add_manager',methods=['POST'])
@required_params(['manager_email'])
@consumer_web_api_check
def add_manager(manager_email):
    user = request.data["auth_user"]
    user.add_manager(manager_email)
    return APIResponse(message='Manager Added', status= HTTPStatus.OK)

@dash_bp.route('/get_all_users', methods=['POST'])
@consumer_web_api_check
def get_all_users():
    user_list = User.get_all()
    if user_list:
        data=[]
        for user in user_list:
            data.append({'name': user.name,'email': user.email,'id':user.id})
        return APIResponse(message='User List Returned', data={'data': data},status=HTTPStatus.OK)
    return APIError(message='No User Found',status=HTTPStatus.NOT_FOUND)

@dash_bp.route('/get_associate',methods=['POST'])
@consumer_web_api_check
def get_associate():
    user = request.data["auth_user"]
    if user.associate:
        associate_list = user.associate
        data = []
        for associate in associate_list:
            data.append({'name': associate.name,'email': associate.email,'id':associate.id})
        return APIResponse(message='Associate List Returned', data={'data': data},status=HTTPStatus.OK)
    return APIError(message='No Associate Found',status=HTTPStatus.NOT_FOUND)

@dash_bp.route('/get_associate_task',methods=['POST'])
@consumer_web_api_check
@required_params(['associate_email', 'selected_date'])
def get_associate_task(associate_email, selected_date):
    associate = User.get_by_email(associate_email)
    if associate.task:
        task_list = associate.task
        data = []
        for task in task_list:
            print(task.name)
            if str(task.created_on.date()) == selected_date:
                data.append({'name': task.name, 'created_on': str(task.created_on.date()),'created_time': str(task.created_on.time()),'created_weekday': task.created_on.weekday() , 'description': task.description,'url': task.url,'end_on': str(task.end_on.date()) if task.end_on else None,'end_time': str(task.end_on.time()) if task.end_on else None,'end_weekday': task.end_on.weekday() if task.end_on else None ,'status': 'completed' if task.end_on else 'in progress', 'id': task.id})
        return APIResponse(message="Task Returned", data={'data': data,'length': len(data)}, status=HTTPStatus.OK)
    return APIError(message='No Task Found', status= HTTPStatus.NOT_FOUND)