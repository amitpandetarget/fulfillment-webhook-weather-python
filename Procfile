web: python app.py
worker:    bundle exec rake resque:work QUEUE=*
urgworker: bundle exec rake resque:work QUEUE=urgent
clock:     bundle exec resque-scheduler