<template>
  <div class="video-mark-wrapper">
    <Hints>
      <template slot="hintName">图片标注</template>
      <template slot="hintInfo">
        <p>标注图片并导出数据</p>
      </template>
    </Hints>

      <div>
    <el-form :model="formInline">
      <el-form-item label="数据集：">
        <el-select v-model="formInline.region" placeholder="选择数据集">
          <el-option
            :label="item.name"
            :value="item.code"
            v-for="item in dataList"
          ></el-option>
        </el-select>
        <el-button type="primary" style="margin-left: 20px" @click="getImg()">选择</el-button>
      </el-form-item>

      <el-form-item label="图片筛选：">
        <el-radio-group v-model="formInline.radio" @change="handleChange">
          <el-radio-button label="全部"></el-radio-button>
          <el-radio-button label="未标注"></el-radio-button>
          <el-radio-button label="已标注"></el-radio-button>
        </el-radio-group>
      </el-form-item>
      <!-- <el-form-item>
        <el-button type="primary">选择</el-button>
      </el-form-item> -->
    </el-form>

    <!-- 图片导航 -->
    <div class="pics">
      <div class="arrow arrow-left" @click="showMore('down')"></div>
      <div class="pic-container">
        <div class="pic-box" ref="picContainer">
          <div class = 'pic' v-for = "(v, i) in imglist">
            <img :src = "'data:img/jpg;base64,' + v"
            @click="activePic('data:img/jpg;base64,' + v)">
          </div>

<!--          <div class="pic" v-for="(v, i) in pics" :key="i">-->
<!--            <div-->
<!--              class="info"-->
<!--              :style="{ 'background-image': 'data:img/jpg;base64,' + v.cropImage }"-->
<!--              @click="activePic(v.cropImage)"-->
<!--            ></div>-->
<!--          </div>-->
        </div>
      </div>
      <div class="arrow arrow-right" @click="showMore('up')"></div>
    </div>

    <el-row :gutter="10" class="tagList">
      <el-col :span="18">
        <ui-marker
          ref="aiPanel-editor"
          class="ai-observer"
          :uniqueKey="uuid"
          :ratio="16 / 9"
          :imgUrl="currentInfo.currentBaseImage"
          @vmarker:onImageLoad="onImageLoad"
        ></ui-marker>
      </el-col>
      <el-col :span="6">
        <div class="title">标签</div>
        <div class="tags" v-for="(v, i) in tags" :key="i">
          <el-tag size="small" @click="setTag(v)">
            {{ v.tagName }}
          </el-tag>
          <i class="el-icon-delete" @click="delTag(i)"></i>
        </div>
        <el-row>
          <el-button type="success" class="handleButton" @click="addTag">
            添加标签
          </el-button>
        </el-row>
        <el-button type="primary" class="handleButton" @click="submitForm">
          提交标注
        </el-button>
      </el-col>
    </el-row>

    <!-- 添加标签 dialog -->
    <el-dialog
      width="30%"
      title="添加标签"
      :visible.sync="innerVisible"
      :before-close="beforeClose"
    >
      <el-form ref="innerForm" :model="innerForm" :rules="tep_rules">
        <el-form-item label="标签名称：" prop="tagName">
          <el-input v-model="innerForm.tagName" />
        </el-form-item>
        <el-form-item label="标签编码：" prop="tag">
          <el-input v-model="innerForm.tag" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="close">取 消</el-button>
        <el-button type="primary" @click="createForm('innerForm')">
          确 定
        </el-button>
      </div>
    </el-dialog>
  </div>
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
      username: localStorage.getItem('username'),
      formInline: {
        region: '',
        radio: '全部'
      },
      dataList: [
        { name: '安全帽', code: 1 },
        { name: '火焰', code: 2 }
      ],

      uuid: '0da9130',
      // 当前图片的信息，包含图片原本的高矮胖瘦尺寸
      currentInfo: {
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
      pics: [
        // {
        //   cropImage: 'https://seopic.699pic.com/photo/50041/3365.jpg_wh1200.jpg'
        // },
        // {
        //   cropImage: 'https://seopic.699pic.com/photo/50041/3365.jpg_wh1200.jpg'
        // },
        // {
        //   cropImage: 'https://seopic.699pic.com/photo/50098/1015.jpg_wh1200.jpg'
        // },
        // {
        //   cropImage: 'https://seopic.699pic.com/photo/50098/1015.jpg_wh1200.jpg'
        // },
        // {
        //   cropImage: 'https://seopic.699pic.com/photo/50050/5027.jpg_wh1200.jpg'
        // },
        // {
        //   cropImage: 'https://seopic.699pic.com/photo/50140/6207.jpg_wh1200.jpg'
        // }
      ],
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
      //
      // Labels: {
      //   filename: '',
      //   height: 0,
      //   width: 0,
      //   xmin: [],
      //   xmax: [],
      //   ymin: [],
      //   ymax: [],
      //   tag: []
      // }
    }
  },
  create(){
    // let parm = Qs.stringify(({'username': this.username}))
    // axios.post('http://127.0.0.1:8000/api/getLabelImg', parm).then(res =>{
    //
    // })

    // this.username = localStorage.getItem("username")
    // let parm = Qs.stringify({'username': localStorage.getItem('username')})
    // getImgList(parm).then(res => {
    //
    // })
  },
  mounted() {
    // let parm = Qs.stringify({
    //   'username': this.username,
    //   // 'user_name': localStorage.getItem("username"),
    // })
    // console.log('mounted')
    // console.log(parm)
    // getImgList(parm).then(res => {
    //   console.log(res.data.code)
    //   this.imglist = res.data.data
    //   console.log(this.imglist)
    //
    // })

    console.log('mounted')
      let parm = Qs.stringify({
        'username': this.username,
      })
      axios.post('http://127.0.0.1:8000/api/getImglist', parm).then(resp => {
        this.imglist = resp.data.data
      })

    console.log(this.pics)

    // this.onImageLoad()

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
      let parm = Qs.stringify({
        'username': this.username,
      })
      axios.post('http://127.0.0.1:8000/api/getImglist', parm).then(resp => {})
    },

    createForm(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          for (let index in this.tags) {
            let item = this.tags[index]
            if (
              item.tagName === this.innerForm.tagName ||
              item.tag === this.innerForm.tag
            ) {
              this.$message.warning('标签名或标签值已存在，请重新输入')
              return
            }
          }
          this.tags.push({
            tagName: this.innerForm.tagName,
            tag: this.innerForm.tag
          })
          this.innerVisible = false
        }
      })
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

      // var element = Qs.stringify({ 'username': this.loginForm.username, 'password': this.loginForm.password })

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
      var parm = Qs.stringify({
        'filename': Labels.filename,
        'width': Labels.width,
        'height': Labels.height,
        'xmin': Labels.xmin,
        'ymin': Labels.ymin,
        'xmax': Labels.xmax,
        'ymax': Labels.ymax,
        'tags': Labels.tag
      }, {indices: false})

      axios.post('http://127.0.0.1:8000/api/label', parm).then(res => {

      })


      // axios.put('http://127.0.0.1:8000/api/label', parm).then(res => {
      //
      // })

    },

    // 点击左右按钮显示更多
    showMore(v) {
      let el = this.$refs.picContainer
      let percent = (this.active / this.pics.length) * 100
      if (v == 'up') {
        this.active++
        if (this.active >= this.picTotal - 3) {
          // 最后4张图
          this.active = this.pics.length - 3
          return
        }
        if (
          this.pics.length - 3 == this.active &&
          this.pics.length < this.picTotal
        ) {
          this.photoPageIndex++
          this.getPhotos()
          return
        }
      } else {
        this.active--
        if (this.active < 0) this.active = 0
      }
      el.style.transform =
        'translateX(-' + (this.active / this.pics.length) * 100 + '%)'
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
    activePic(v) {
      console.log('active')
      this.currentInfo.currentBaseImage = v
      let im = new Image;
      im.src = v
      this.imageInfo = {rawW: im.width, rawH: im.height}
    },

    handleChange(label) {
      console.log(label)
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
  }
}
</style>
