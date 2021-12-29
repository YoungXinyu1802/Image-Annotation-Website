<template>
  <div class="video-mark-wrapper">
    <Hints>
      <template slot="hintName">图片标注</template>
      <template slot="hintInfo">
        <p>标注图片并导出数据，可以新建标签，标签需要为英文</p>
      </template>
    </Hints>

    <el-row :gutter="10" class="tagList">
      <el-col :span="16">
        <el-card shadow="always" class = "el-card">
          <div slot="header" class="title">标注区域</div>
        <ui-marker
          ref="aiPanel-editor"
          class="ai-observer"
          :uniqueKey="uuid"
          :ratio="16 / 9"
          :imgUrl="currentInfo.currentBaseImage"
          @vmarker:onImageLoad="onImageLoad"
        ></ui-marker>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="always" class = "el-card">
          <div slot="header" class="title">工具栏</div>
    <el-form :model="formInline">
      <el-form-item label="任务：">
        <el-select v-model="formInline.region" placeholder="选择任务">
          <el-option
            :label="item.name"
            :value="item.name"
            v-for="item in dataList"
          ></el-option>
        </el-select>
        <el-button type="primary" style="margin-left: 20px" @click="getImg()">选择</el-button>
      </el-form-item>

      <el-form-item label="选择导出格式：">
       <el-radio-group v-model="formInline.radio" @change="handleChange">
          <el-radio-button label="PascalVoc"></el-radio-button>
          <el-radio-button label="createML"></el-radio-button>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="标签">
        <el-tag
          :key="tag"
          v-for="tag in dynamicTags"
          closable
          :disable-transitions="false"
          @click="setTag(tag)"
          @close="handleClose(tag)">
          {{tag}}
        </el-tag>
        <el-input
          class="input-new-tag"
          v-if="inputVisible"
          v-model="inputValue"
          ref="saveTagInput"
          size="small"
          @keyup.enter.native="handleInputConfirm"
          @blur="handleInputConfirm"
        >
        </el-input>
        <el-button v-else class="button-new-tag" size="small" @click="showInput">+ New Tag</el-button>
      </el-form-item>
      <el-form-item>
        <el-carousel trigger="click" height="150px" autoplay="false" class="carousel">
          <el-carousel-item v-for = "v in imglist">
            <img :src = "'data:img/jpg;base64,' + v.b64"
                @click="activePic('data:img/jpg;base64,' + v.b64, v.filename)" alt="">
          </el-carousel-item>
        </el-carousel>
      </el-form-item>
      <el-form-item>
        <el-button @click="submitForm" type="primary">提交</el-button>
      </el-form-item>
    </el-form>

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
import { AIMarker } from 'vue-picture-bd-marker'
import { getImgList } from '../api'

export default {
  name: 'VideoMark',
  components: {'ui-marker': AIMarker, Hints, ElementDrr, TextSetting},
  data() {
    return {
      dynamicTags: [],
              inputVisible: false,
        inputValue: '',
      username: localStorage.getItem('username'),
      formInline: {
        region: '',
        radio: 'PascalVoc'
      },
      dataList: [],

      uuid: '0da9130',
      // 当前图片的信息，包含图片原本的高矮胖瘦尺寸
      currentInfo: {
        currentFilename: '',
        currentBaseImage:
          '',
        rawW: 0,
        rawH: 0,
        currentW: 0,
        currentH: 0,
        checked: false, // false表示当前图片还没有标记过
        data: [] // 表示图片矩形标记信息
      },
      imglist: [],

      // *****************************
      pics: [],
      active: 0, // 当前图片序号
      picTotal: 10, // 照片总数

      // *********************************************
      tags: [
        {
          tagName: 'bee',
          tag: '0x0001'
        },
        {
          tagName: 'car',
          tag: '0x0002'
        }
      ],
      allInfo: [], // 图片的矩形标记信息集合
      imageInfo: [], // 存储图片原始信息

      innerVisible: false,
      innerForm: {
        tagName: '',
        tag: ''
      },

      tep_rules: {
        tagName: [{ required: true, message: '请输入', trigger: 'blur' }],
        tag: [{ required: true, message: '请输入', trigger: 'blur' }]
      },
    }
  },
  create(){
  },
  mounted() {
    let parm = Qs.stringify(({'username': this.username}))
    const _this = this
    axios.post('http://127.0.0.1:8000/api/getUserTask', parm).then(
      function(res) {
        console.log(res.data.data)
        for (let i = 0; i < res.data.data.length; i++) {
          let temp = {name: res.data.data[i], code: i}
          _this.dataList.push(temp)
        }
      }
    )
    console.log(this.dataList)
  },
  methods: {
    /**记录图片当前的大小和原始大小 data={rawW,rawH,currentW,currentH} */
    onImageLoad(data) {
      console.log('data')
      console.log(data)
      this.imageInfo = data
    },

    setTag(v) {
      this.$refs['aiPanel-editor'].getMarker().setTag(v)
    },
    addTag() {
      this.innerVisible = true
      this.innerForm.tagName = ''
      this.innerForm.tag = ''
    },
    delTag(index) {
      this.tags.splice(index, 1)
    },
    close() {
      this.innerVisible = false
      this.$refs['innerForm'].resetFields()
    },
    beforeClose(done) {
      this.$refs['innerForm'].resetFields()
      done()
    },
    getImg(){
      this.imglist = []
      console.log(this.formInline.region)
      let parm = Qs.stringify({
        'username': this.username,
        'taskname': this.formInline.region
      })
      console.log('getImg')
      axios.post('http://127.0.0.1:8000/api/getImglist', parm).then(resp => {
        // this.imglist = resp.data.base64
        console.log(resp.data.filename)
        for(let i = 0; i < resp.data.filename.length; i++) {
          let parm = {filename: resp.data.filename[i], b64: resp.data.base64[i]}
          this.imglist.push(parm)
        }
      })
      console.log(this.imglist)
    },
    /**
     * 完成标记，提交标记集合
     */
    submitForm() {
      let Labels = {
        filename: '',
        height: 0,
        width: 0,
        xmin: [],
        xmax: [],
        ymin: [],
        ymax: [],
        tag: []
      }
      let data = this.$refs['aiPanel-editor'].getMarker().getData()

      this.allInfo = data
      console.log(this.allInfo)

      console.log(this.allInfo.length, '个数')

      let size = {
        width: this.imageInfo.rawW,
        height: this.imageInfo.rawH
      }
      console.log(size)

      Labels.width = size.width
      Labels.height = size.height

      for (let i = 0; i < this.allInfo.length; i++) {
        console.log(i)
        let xmin =
          ((parseInt(this.allInfo[i].position.x
            .substring(0, this.allInfo[i].position.x.length - 1)) * size.width) / 100)
            .toFixed(0).toString()
        console.log(xmin, '左上')
        let ymin =
          ((parseInt(this.allInfo[i].position.y
            .substring(0, this.allInfo[i].position.y.length - 1)) * size.height) / 100)
            .toFixed(0).toString()
        console.log(ymin, '右手上')
        let xmax =
          ((parseInt(this.allInfo[i].position.x1
            .substring(0, this.allInfo[i].position.x1.length - 1)) * size.width) / 100)
            .toFixed(0).toString()
        console.log(xmax, '右上')
        let ymax =
          ((parseInt(this.allInfo[i].position.y1
            .substring(0, this.allInfo[i].position.y1.length - 1)) * size.height) / 100)
            .toFixed(0).toString()
        console.log(ymax, '左上')

        let tag = this.allInfo[i].tagName
        console.log(tag)

        Labels.xmin.push(xmin)
        Labels.xmax.push(xmax)
        Labels.ymin.push(ymin)
        Labels.ymax.push(ymax)
        Labels.tag.push(tag)
      }
      console.log(Labels)
      console.log('file label')
      console.log(this.currentInfo.currentFilename)
      let parm = Qs.stringify({
        'taskname': this.formInline.region,
        'filename': this.currentInfo.currentFilename,
        'type': this.formInline.radio,
        'width': Labels.width,
        'height': Labels.height,
        'xmin': Labels.xmin,
        'ymin': Labels.ymin,
        'xmax': Labels.xmax,
        'ymax': Labels.ymax,
        'tags': Labels.tag
      }, {indices: false})

      axios.post('http://127.0.0.1:8000/api/label', parm).then(res => {
        console.log(res.data)
        if(res.data.code === 0){
          this.$message.success("提交成功")
        }
        else{
          this.$message.error("提交失败")
        }

      })
    },


    getPhotos() {
      return this.$nextTick(() => {
        let el = this.$refs.picContainer
        if (el) {
          el.style.width = el.scrollWidth + 'px'

          el.style.transform =
            'translateX(-' + (this.active / this.pics.length) * 100 + '%)'
        }
      })
    },
    /**得到当前点击图片*/
    activePic(v, f) {
      console.log('active')
      this.currentInfo.currentBaseImage = v
      let im = new Image;
      im.src = v
      console.log(f)
      this.currentInfo.currentFilename = f
      this.imageInfo = {rawW: im.width, rawH: im.height}
      console.log(this.currentInfo.currentFilename)
    },

    handleChange(label) {
      console.log(label)
      this.formInline.radio=label
    },
      handleClose(tag) {
        this.dynamicTags.splice(this.dynamicTags.indexOf(tag), 1);
      },

      showInput() {
        this.inputVisible = true;
        this.$nextTick(_ => {
          this.$refs.saveTagInput.$refs.input.focus();
        });
      },

      handleInputConfirm() {
        let inputValue = this.inputValue;
        if (inputValue) {
          this.dynamicTags.push(inputValue);
        }
        this.inputVisible = false;
        this.inputValue = '';
      }

  }
}
</script>

<style lang="less">
.video-mark-wrapper {
  .pics {
    width: 100%;
    overflow: hidden;
    margin-bottom: 20px;
    display: flex;
    justify-content: center;
    align-items: center;

    .arrow {
      width: 20px;
      height: 20px;
      border-radius: 50%;
      //background-image: url('~@/assets/images/common/left.png');
      background-repeat: no-repeat;
      background-size: contain;

      &.arrow-right {
        transform: rotate(180deg);
      }
    }

    .pic-container {
      // width: 1180px;
      width: calc(100% - 30px);
      height: 114px;
      margin: 0 auto;
      overflow: hidden;

      .pic-box {
        height: 100%;
        // min-width: 1180px;
        min-width: calc(100% - 30px);
        transition: all 0.5s linear;
        display: flex;
        flex-wrap: nowrap;
      }

      .pic {
        float: left;
        border: 1px solid #ccc;
        box-sizing: border-box;
        margin-right: 10px;
        width: 185px;
        height: 114px;

        .info {
          width: 183px;
          height: 100%;
          background-size: 100%;
          background-repeat: no-repeat;
          background-position: center;
          position: relative;

          &:hover {
            border: 1px solid skyblue;
          }
        }
      }
    }
  }

  .tagList {
    .title {
      text-align: center;
      font-weight: bold;
    }

    .handleButton {
      width: 100%;
      margin-bottom: 10px;
    }

    .tags {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 10px 0;

      .el-icon-delete {
        cursor: pointer;
      }
    }
    .carousel{
      margin-top: 20px;
    }
    .el-card{
      height: 530px;
    }
  }
}
</style>
