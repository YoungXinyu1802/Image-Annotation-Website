<template>
  <div class="video-mark-wrapper">
    <Hints>
      <template slot="hintName">上传视频</template>
      <template slot="hintInfo">
        <p>上传视频后，点击截取有效帧</p>
      </template>
    </Hints>
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card shadow="always" class="card">
          <div slot="header" class="title">视频区域</div>
          <div>
          <input type="file" @change="getBigectURL($event)" />
          </div>
          <video :src="videoSrc" controls="controls" width="500" height="400"></video>

        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="always" class="card">
          <div slot="header" class="title">提取区域</div>
        <div>
            <el-button type="primary" @click="cutPicture">
                截图
            </el-button>
            <el-button type="primary" @click="commit">
                提交
            </el-button>
            <el-button @click="cancel">
                取消
            </el-button>
        </div>
        <canvas id="myCanvas" width="343" height="200"></canvas>
          <el-carousel :interval="4000" type="card" height="200px">
            <el-carousel-item v-for="(item, i) in imgSrc">
              <img v-bind:src="item" alt="" class = img>
            </el-carousel-item>
          </el-carousel>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import Hints from '../components/Hints'
import ElementDrr from '../components/ElementDrr'
// import ImageRichText from '../components/ImageRichText'
import TextSetting from '../components/TextSetting'
// import UploadImage from '../components/UploadImage'
import {calcImageSize} from '../utils'

import Qs from "qs";
import axios from "axios";

export default {
  name: 'VideoMark',
  components: {Hints, ElementDrr, TextSetting},
  data() {
    return {
      username: localStorage.getItem('username'),
      videoSrc:'',
      imgSrc: []
    }
  },
  methods: {
    cutPicture() {
      let self = this;
      var v = document.querySelector("video");
      let canvas = document.getElementById('myCanvas')
      var ctx = canvas.getContext('2d');
      ctx.drawImage(v, 0, 0, 343, 200);
      var oGrayImg = canvas.toDataURL('image/jpeg');
      // this.imgSrc = oGrayImg
      this.imgSrc.push(oGrayImg)
    },
    getBigectURL (event) {
      console.log('getBigectURL', event)
      var current = event.target.files[0]
      var fileReader = new FileReader()
      fileReader .readAsDataURL(current)
      var that = this
      fileReader.onload = function (e) {
        that.videoSrc = e.currentTarget.result
        console.log(that.videoSrc)
      }
    },

    commit(){
      var parm = Qs.stringify({
        'username': this.username,
        'videoSrc': this.videoSrc,
        'imgSrc': this.imgSrc
      }, {indices: false})

      axios.post('http://127.0.0.1:8000/api/video2img', parm).then(res => {
        this.$message.success('上传成功')
      })

    },
    cancel(){
      this.imgSrc = []
    }

  }
}
</script>

<style lang="less">
.video-mark-wrapper {
  .card{
    height: 530px
  }
  .box-wrapper {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 550px;
    overflow: hidden;

    .drag-container {
      position: relative;
      width: 850px;
      height: 478px;

      video {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
      }

      .z-drr-container {
        border: 1px dashed transparent;

        &.z-active {
          border: 1px dashed #2e95ff;
        }
      }
    }
  }

  .box-content {
    height: 550px;
    overflow: hidden;

    .form-wrapper {
      width: 300px;
      margin: 50px auto 0;
    }

    .el-button {
      width: 210px;
    }
  }
  .box{
    //margin-top: 10px;
    .ul{
      display: flex;
      flex-wrap: wrap;
      position: relative;
      margin-top: 10px
    }
    .li{
      padding: 3px;
      list-style: none;
      margin-right: 15px;
    }
    .img{
      width: 200px;
      height: 150px
    }
  }

}
</style>
