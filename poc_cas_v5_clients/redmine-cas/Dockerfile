FROM redmine:3.3

WORKDIR /usr/src/redmine/plugins
#RUN git clone https://github.com/pbelikov/redmine-omniauth-oauth-cas.git && mv redmine-omniauth-oauth-cas redmine_omniauth_isu 
RUN git clone https://github.com/ninech/redmine_cas
#RUN git clone https://github.com/devopskube/redmine_openid_connect 
WORKDIR /usr/src/redmine
RUN bundle install
#RUN bundle exec rake redmine:plugins:migrate RAILS_ENV=production
