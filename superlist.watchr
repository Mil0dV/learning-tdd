watch( '.*\.py' ) do
  system 'python manage.py test'
end