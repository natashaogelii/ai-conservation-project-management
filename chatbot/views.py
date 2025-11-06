from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from projects.models import Project, ProjectTeamMembership
from django.db.models import Sum
import csv, os, json

@method_decorator(csrf_exempt, name='dispatch')
class ChatbotView(View):
    def get_response(self, user_input):
        user_input = user_input.lower()

        # --- Handle dynamic project-based responses ---
        try:
            # 1️⃣ Query for all projects
            projects = Project.objects.all()
            if not projects.exists():
                return "There are currently no projects in the system."

            # 2️⃣ Handle multi-project queries
            if "total budget" in user_input:
                total = projects.aggregate(Sum('budget'))['budget__sum'] or 0
                return f"The total budget for all projects is ${total:,.2f}."

            elif "how many projects" in user_input or "number of projects" in user_input:
                return f"There are currently {projects.count()} projects in the system."

            elif "list" in user_input and "project" in user_input:
                titles = [p.title for p in projects]
                return "Here are all the project titles: " + ", ".join(titles)

            # 3️⃣ For single-project details (latest project)
            project = projects.last()

            if "title" in user_input:
                return f"The latest project is titled '{project.title}'."

            elif "budget" in user_input:
                return f"The project budget is ${project.budget:,.2f}."

            elif "remaining" in user_input:
                remaining = getattr(project, "remaining_budget", None)
                return f"The remaining budget is ${remaining:,.2f}." if remaining else "Remaining budget not available."

            elif "spent" in user_input or "expenses" in user_input:
                total_spent = getattr(project, "total_spent", None)
                return f"So far, ${total_spent:,.2f} has been spent on this project." if total_spent else "Expense details not available."

            elif "start" in user_input:
                return f"The project starts on {project.start_date.strftime('%B %d, %Y')}."

            elif "end" in user_input or "finish" in user_input or "deadline" in user_input:
                return f"The project ends on {project.end_date.strftime('%B %d, %Y')}."

            elif "description" in user_input or "about" in user_input:
                return f"Here’s what the project is about: {project.description}"

            elif "progress" in user_input or "complete" in user_input:
                return f"The project is {project.progress}% complete."

            elif "team" in user_input or "members" in user_input:
                members = ProjectTeamMembership.objects.filter(project=project)
                if members.exists():
                    names = [f"{m.user.username} ({m.get_role_display()})" for m in members]
                    return "The project team members are: " + ", ".join(names)
                else:
                    return "There are no team members assigned yet."

            elif "task" in user_input or "tasks" in user_input:
                tasks = project.tasks.all()
                if tasks.exists():
                    task_list = [f"{t.title} (Due {t.due_date.strftime('%b %d')})" for t in tasks]
                    return "Here are the tasks: " + "; ".join(task_list)
                else:
                    return "No tasks have been added yet."

            else:
                # fallback handled below
                pass

        except Exception as e:
            return f"Oops! Something went wrong: {str(e)}"

        # --- Fallback to static CSV responses ---
        try:
            csv_path = os.path.join(os.path.dirname(__file__), "qa.csv")
            if os.path.exists(csv_path):
                with open(csv_path, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if user_input in row["Question"].lower():
                            return row["Answer"]
        except Exception:
            pass

        return "I’m not sure about that. You can ask things like the project budget, progress, team members, or tasks."

    def post(self, request):
        # Handle both JSON fetch and form POST
        try:
            if request.body:
                data = json.loads(request.body)
                user_input = data.get("message", "")
            else:
                user_input = request.POST.get("message", "")
        except json.JSONDecodeError:
            user_input = request.POST.get("message", "")

        response = self.get_response(user_input)
        return JsonResponse({'response': response})
