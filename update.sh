has_updated="Already"

# update backend code
echo '从git上更新后端代码...'
cd /library/library-management-backend
backend_is_update=$(git pull | awk '{print $1}')
echo '从git上更新后端代码完成'

if [ "$backend_is_update" != "$has_updated" ]; then
  ps -ef | grep python | grep -v grep | awk '{print $2}' | sed -e "s/^/kill -9 /g" | sh -
else
  echo '后端无需打包'
fi

python_pid=$(ps -ef | grep python | grep -v grep | awk '{print $2}')

if [ ! -n "$python_pid" ]; then
  echo '启动python应用...'
  cd /library/library-management-backend
  echo | nohup python manage.py runserver 0.0.0.0:8000 &
fi
tail -f /library/library-management-backend/nohup.out
