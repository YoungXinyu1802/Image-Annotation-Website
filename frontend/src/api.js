import axios from 'axios'

export function getTableList(param) {
  return axios({
    url: 'http://127.0.0.1:8000/api/getTasklist',
    method: 'post',
    param
  })
}

export function getImgList(param) {
  console.log('post')
  return axios({
    url: 'http://127.0.0.1:8000/api/getImglist',
    method: 'post',
    param
  })
}

export function getTaskImg(param) {
  console.log('post')
  return axios({
    url: 'http://127.0.0.1:8000/api/getTaskImg',
    method: 'post',
    param
  })
}
