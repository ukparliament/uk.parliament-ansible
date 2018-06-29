from checks import AgentCheck

import json

class GoogleAnalyticsCheck(AgentCheck):
  def check(self,instance):
    with open('/opt/google-analytics/google-analytics.json') as json_data:
      data = json.load(json_data)
      beta_active_users = data["rt"][0]["beta-active-users"]
      www_active_users = data["rt"][1]["www-active-users"]

      self.gauge('parliament.beta.users', beta_active_users)
      self.gauge('parliament.www.users', www_active_users)
