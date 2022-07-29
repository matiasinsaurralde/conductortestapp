from flask import Flask, request, jsonify, abort
import jwt
import re
import os, subprocess, time

def create_app():
  app = Flask(__name__)

  @app.get("/v1/user")
  def get_user():
    res = {
      'user_id': request.decoded_jwt['user_id'],
      'user_full_name': request.decoded_jwt['user_full_name'],
      'user_email': request.decoded_jwt['user_email'],
    }
    return jsonify(res)

  @app.get("/healthz")
  def healthz():
    return "", 402

  @app.post("/execute")
  def execute():
    # Hold global env vars here:
    input = request.json
    global_env = {}
    for k, v in input["env"].items():
      global_env[k] = v
    task_state = {}
    priority_tasks = []
    secondary_tasks = []
    task_outputs = []
    for task in input["tasks"]:
      if len(task["dependsOn"]) == 0:
        priority_tasks.append(task)
      else:
        secondary_tasks.append(task)
    for task in priority_tasks:
      local_env = {}
      for k, v in task["env"].items():
        if v == '':
          local_env[k] = global_env[k]
        else:
          local_env[k] = v
      t1 = time.time()
      cmd_output = subprocess.run(task["command"], shell=True, env=local_env)
      t2 = time.time()
      timeDiff = t2 - t1
      task_output = {"id": task["id"], "exitCode": cmd_output.returncode, "elapsedTime": timeDiff, "output": cmd_output.stdout}
      if cmd_output.returncode == 0:
        task_output["status"] = 'success'
      else:
        task_output["status"] = 'failed'
      task_state[task["id"]] = cmd_output.returncode
      task_outputs.append(task_output)
    print(task_state)
    for task in secondary_tasks:
      successful_deps = 0
      for dep in task["dependsOn"]:
        st = task_state[dep]
        if st == 0:
          successful_deps += 1
      print("Trying to run task", task, "successful_deps=", successful_deps, "total_deps=", len(task["dependsOn"]))
      # if len(task["dependsOn"]) 
    return jsonify(task_outputs)
  return app