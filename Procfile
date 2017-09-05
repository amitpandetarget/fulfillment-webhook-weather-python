web: python app.py
worker:        env QUEUE=* bundle exec rake resque:work
urgentworker:  env QUEUE=urgent bundle exec rake resque:work