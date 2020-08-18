# Copyright 2019 The Casbin Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import casbin
from django.core.exceptions import PermissionDenied


class CasbinMiddleware:
    """
    Casbin middleware.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # Initialize the Casbin enforcer, executed only on once.
        self.enforcer = casbin.Enforcer("casbin_middleware/authz_model.conf", "casbin_middleware/authz_policy2.csv")
        a = mysqladapter.DBAdapter("mysql", "mysql_username:mysql_password@tcp(127.0.0.1:3306)/")
        e = casbin.Enforcer("path/to/basic_model.conf", a)

    def __call__(self, request):
        # Check the permission for each request.
        if not self.check_permission(request):
            # Not authorized, return HTTP 403 error.
            self.require_permission()

        # Permission passed, go to next module.
        response = self.get_response(request)
        return response

    def check_permission(self, request):
        # Customize it based on your authentication method.
        user = request.user.username
        if request.user.is_anonymous:
            user = 'anonymous'
        path = request.path
        method = request.method
        # select by strategy -> sub, obj, act
        user = dict()
        user['Age'] = 25
        user['name'] = 'jemco3'
        user['id'] = 5

        path = dict()
        path['ownerId'] = 5
        method = 'read'
        model_text = """
        [request_definition]
        r = sub, obj, act
        
        [policy_definition]
        p = sub, obj, act
        
        [policy_effect]
        e = some(where (p.eft == allow))
        
        [matchers]
        # m = r.sub.Age > 18 && r.sub.Age < 60 && r.sub.id == r.obj.ownerId && r.act == p.act
        m = r.sub.name == p.sub.name
        """
        model = self.enforcer.new_model(text=model_text)
        self.enforcer.set_model(m=model)

        return self.enforcer.enforce(user, path, method)

    def require_permission(self,):
        raise PermissionDenied
