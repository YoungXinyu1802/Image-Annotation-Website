<template>
  <div class="image-cropper-wrapper">
    <Hints>
      <template slot="hintName">图片裁剪插件</template>
      <template slot="hintInfo">
        <p>Vue-Cropper：一个优雅的图片裁剪插件，可实现图片裁剪、图片生成等功能，并支持生成png、jpeg、webp等图片格式</p>
        <p>github地址：访问 <el-link type="success" href="https://github.com/xyxiao001/vue-cropper" target="_blank">Vue-Cropper</el-link></p>
      </template>
    </Hints>
   <el-card shadow="always">
      <div slot="header" class="el-card-header">
        <h2 class="login-title">上传图片</h2>
      </div>
     <el-form>
       <el-form-item label="数据集名称">
         <el-input v-model="database" placeholder="请输入内容" class = "el-input"></el-input>
       </el-form-item>
      <el-upload
        name = 'file'
        ref="upload"
        action="http://127.0.0.1:8000/api/upload"
        :data="{username:this.username, database: this.database}"
        list-type="picture-card"
        :before-upload="beforeAvatarUpload"
        multiple
        :auto-upload="false"
      >
          <i slot="default" class="el-icon-plus"></i>
          <div slot="file" slot-scope="{file}">
            <img
              class="el-upload-list__item-thumbnail"
              :src="file.url" alt=""
            >
            <span class="el-upload-list__item-actions">
              <span
                class="el-upload-list__item-preview"
                @click="handlePictureCardPreview(file)"
              >
                <i class="el-icon-zoom-in"></i>
              </span>
              <span
                v-if="!disabled"
                class="el-upload-list__item-delete"
                @click="handleDownload(file)"
              >
                <i class="el-icon-download"></i>
              </span>
              <span
                v-if="!disabled"
                class="el-upload-list__item-delete"
                @click="handleRemove(file)"
              >
                <i class="el-icon-delete"></i>
              </span>
            </span>
          </div>
      </el-upload>
      <el-dialog :visible.sync="dialogVisible">
        <img width="100%" :src="dialogImageUrl" alt="">
      </el-dialog>
       </el-form>
    </el-card>
    <el-button type="primary" class="submit-button" @click="submitUpload">创建</el-button>

  </div>
</template>

<script>
import { VueCropper } from 'vue-cropper'
import Hints from '../components/Hints'
import UploadImage from '../components/UploadImage'

export default {
  name: 'ImageCropper',
  components: { Hints, VueCropper, UploadImage },
  data() {
    return {
        username: localStorage.getItem('username'),
        inputVisible: false,
        inputValue: '',

        dialogImageUrl: '',
        dialogVisible: false,
        disabled: false,

        database: ''

    }
  },
  methods: {
    downloadImage() {
      this.$refs.cropper.getCropBlob(data => {
        this.downImg = window.URL.createObjectURL(data)
        if (window.navigator.msSaveBlob) {
          const blobObject = new Blob([data])
          window.navigator.msSaveBlob(blobObject, 'demo.png')
        } else {
          this.$nextTick(() => {
            this.$refs.downloadDom.click()
          })
        }
      })
    },
      submitUpload() {
        console.log('submit!');
        console.log(this.username)
        this.$refs.upload.submit()
      },


  }
}
</script>

<style lang="less">
.image-cropper-wrapper{
  .el-input{
    width: 80%
  }

  .submit-button{
      position: relative;
      margin-top: 10px
  }
}


</style>
