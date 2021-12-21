<template>
  <div class="video-mark-wrapper">
    <Hints>
      <template slot="hintName">视频水印</template>
      <template slot="hintInfo">
        <p>基于VueDRR拖拽功能，在视频上通过叠加图片、文字等，实现视频添加水印的功能</p>
        <p>VueDRR：基于vue-draggable-resizable的vue组件，可以实现拖动、拉伸和旋转功能</p>
      </template>
    </Hints>
    <el-row :gutter="20">
      <el-col :span="16">
        <el-card shadow="always">
          <div slot="header" class="title">合成区域</div>
          <div class="box-wrapper">
            <div class="drag-container">
              <video :src="videoSrc" controls/>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="always">
          <div slot="header" class="title">设置区域</div>
        <div>
            <el-button @click="cutPicture">
                截图
            </el-button>
            <el-button @click="commit">
                提交
            </el-button>
        </div>
        <canvas id="myCanvas" width="343" height="200"></canvas>
      <div class="box">
        <ul class = 'ul'>
          <li v-for="(item, i) in imgSrc" class = 'li'>
            <img v-bind:src="item" alt="" class = img>
          </li>
        </ul>
	    </div>


        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import Hints from '../../components/Hints'
import ElementDrr from '../../components/ElementDrr'
import ImageRichText from '../../components/ImageRichText'
import TextSetting from '../../components/TextSetting'
import UploadImage from '../../components/UploadImage'
import {calcImageSize} from '../../utils'

import Qs from "qs";
import axios from "axios";

export default {
  name: 'VideoMark',
  components: {Hints, ElementDrr, ImageRichText, TextSetting, UploadImage},
  data() {
    return {
      // videoSrc: 'https://cdn.jsdelivr.net/gh/baimingxuan/media-store/videos/houlang.mp4',
      username: localStorage.getItem('username'),
      videoSrc: require("../../assets/video/video.mp4"),
      // elements: [], // 叠加组件数组
      // activeEle: {}, // 当前图片上聚焦的叠加组件
      // eleNum: 0,
      imgSrc: []
    }
  },
  computed: {
    // 选择的文本
    activeEleText() {
      if (this.activeEle.type === 'text') {
        return this.activeEle
      }
    }
  },
  created() {
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

    commit(){
      var parm = Qs.stringify({
        'username': this.username,
        'videoSrc': this.videoSrc,
        'imgSrc': this.imgSrc
      }, {indices: false})

      axios.post('http://127.0.0.1:8000/api/video2img', parm).then(res => {

      })

    }

  }
}
</script>

<style lang="less">
.video-mark-wrapper {
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
