import axios from 'axios'

export function getTableList(param) {
  return axios({
    url: 'http://127.0.0.1:8000/api/getTasklist',
    method: 'get',
    param
  })
}
