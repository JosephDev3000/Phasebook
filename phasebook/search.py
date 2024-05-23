from flask import Blueprint, request

from .data.search_data import USERS


bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("")
def search():
    return search_users(request.args.to_dict()), 200


def search_users(args):
    """Search users database

    Parameters:
        args: a dictionary containing the following search parameters:
            id: string
            name: string
            age: string
            occupation: string

    Returns:
        a list of users that match the search parameters
    """

    id = args.get("id")
    name = args.get("name", "").lower()
    age = args.get("age")
    occupation = args.get("occupation", "").lower()

    result = []

    match_priority = []

    if id:
        
        user = next((user for user in USERS if user["id"] == id), None)
        if user:
            result.append(user)
            match_priority.append((user, 'id'))

    for user in USERS:
        if user in result:
            continue  

        matched_by = None
        if name and name in user["name"].lower():
            matched_by = 'name'
        if age and int(age) - 1 <= user["age"] <= int(age) + 1:
            matched_by = 'age'
        if occupation and occupation in user["occupation"].lower():
            matched_by = 'occupation'

        if matched_by:
            result.append(user)
            match_priority.append((user, matched_by))

    
    def get_priority(match):
        user, criteria = match
        priority = {
            'id': 0,
            'name': 1,
            'age': 2,
            'occupation': 3
        }
        return priority[criteria]

    sort_result = sorted(match_priority, key=get_priority)
    sort_users = [match[0] for match in sort_result]

    return sort_users
