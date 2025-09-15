from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models import Task
from datetime import datetime

tasks = Blueprint("tasks", __name__)

# Create Task
@tasks.route("/addtask", methods=["POST"])
@jwt_required()
def create_task():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        deadline = None
        if 'deadline' in data and data['deadline']:
            try:
                deadline = datetime.strptime(data['deadline'], "%Y-%m-%d")
            except ValueError:
                return jsonify({"error": "Invalid date format, expected YYYY-MM-DD"}), 400

        new_task = Task(
            title=data.get("title"),
            content=data.get("content"),
            status=data.get("status", "Pending"),
            deadline=deadline,
            user_id=user_id
        )

        db.session.add(new_task)
        db.session.commit()

        return jsonify({"message": "Task created", "task_id": new_task.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Get All Tasks
@tasks.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    try:
        user_id = get_jwt_identity()
        tasks_list = Task.query.filter_by(user_id=user_id).all()

        result = [
            {
                "id": t.id,
                "title": t.title,
                "content": t.content,
                "status": t.status,
                "created_at": t.created_at.isoformat(),
                "deadline": t.deadline.isoformat() if t.deadline else None
            } for t in tasks_list
        ]
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update Task
@tasks.route("/tasks/<string:task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    try:
        user_id = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=user_id).first_or_404()

        data = request.get_json()
        task.title = data.get("title", task.title)
        task.content = data.get("content", task.content)
        task.status = data.get("status", task.status)

        # Parse deadline if provided
        if "deadline" in data and data["deadline"]:
            try:
                task.deadline = datetime.strptime(data["deadline"], "%Y-%m-%d")
            except ValueError:
                return jsonify({"error": "Invalid date format, expected YYYY-MM-DD"}), 400

        db.session.commit()
        return jsonify({"message": "Task updated"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Delete Task
@tasks.route("/tasks/<string:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    try:
        user_id = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=user_id).first_or_404()

        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
# Get Single Task
@tasks.route("/tasks/<string:task_id>", methods=["GET"])
@jwt_required()
def get_task(task_id):
    try:
        user_id = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=user_id).first_or_404()

        result = {
            "id": task.id,
            "title": task.title,
            "content": task.content,
            "status": task.status,
            "created_at": task.created_at.isoformat(),
            "deadline": task.deadline.isoformat() if task.deadline else None
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500