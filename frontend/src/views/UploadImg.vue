<template>
  <div class="image-cropper-wrapper">
    <Hints>
      <template slot="hintName">图片上传</template>
      <template slot="hintInfo">
        <p>选择本地图片上传，图片格式为jpg，大小不能超过5M</p>
      </template>
    </Hints>
   <el-card shadow="always">
      <div slot="header" class="el-card-header">
        <h2 class="login-title">上传图片</h2>
      </div>
     <el-form>
<!--       <el-form-item label="数据集名称">-->
<!--         <el-input v-model="database" placeholder="请输入内容" class = "el-input"></el-input>-->
<!--       </el-form-item>-->
      <el-upload
        name = 'file'
        ref="upload"
        action="http://127.0.0.1:8000/api/upload"
        :data="{username:this.username, database: this.database}"
        list-type="picture-card"
        :before-upload="beforeAvatarUpload"
        multiple
        :on-remove="handleRemove"
        :before-remove="beforeRemove"
        :auto-upload="false"
      >
          <i slot="default" class="el-icon-plus"></i>
          <div slot="file" slot-scope="{file}">
            <img
              class="el-upload-list__item-thumbnail"
              :src="file.url" alt=""
            >
          </div>
      </el-upload>
      <el-dialog :visible.sync="dialogVisible">
        <img width="100%" :src="dialogImageUrl" alt="">
      </el-dialog>
       </el-form>
    </el-card>
    <el-button type="primary" class="submit-button" @click="submitUpload">上传</el-button>
    <el-button class="submit-button" @click="resetImg">取消</el-button>

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
        valid: true,
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
      handleRemove(file, fileList) {
        console.log(file, fileList);
      },
      beforeRemove(file, fileList) {
        return this.$confirm(`确定移除 ${ file.name }？`);
      },

      // handleRemove(file) {
      //     console.log(file);
      // },
      beforeAvatarUpload(file) {
        const isJPG = file.type === 'image/jpeg';
        const isLt5M = file.size / 1024 / 1024 < 5;

        if (!isJPG) {
          this.$message.error('上传图片只能是 JPG 格式!');
        }
        if (!isLt5M) {
          this.$message.error('上传图片大小不能超过 5MB!');
        }
        this.valid = isJPG && isLt5M
        return isJPG && isLt5M;
      },

      submitUpload() {
        console.log('submit!');
        console.log(this.username)
        this.$refs.upload.submit()
        if(this.valid){
          this.$message.success('上传成功')
          this.$refs.upload.clearFiles()
        }

      },
      resetImg() {
        this.$refs.upload.clearFiles()
      }
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
