<template>
  <div class="form-list-wrapper">
    <Hints>
      <template slot="hintName">Form表单组件</template>
      <template slot="hintInfo">
        <p>element-Form：使用elementUI的Form组件，可用以收集、校验和提交数据等操作</p>
        <p>地址：访问 <el-link type="success" href="https://element.eleme.cn/2.13/#/zh-CN/component/form" target="_blank">element-Form</el-link></p>
      </template>
    </Hints>
    <el-card shadow="always" class = "el-card">
      <div slot="header" class="el-card-header">
        <h2 class="login-title">任务信息</h2>
      </div>
    <el-form ref="form" :model="task" label-width="80px">
      <el-form-item label="任务名称">
        <el-input
          v-model="task.name"
          maxlength="10"
          show-word-limit
          class = "el-input"
        >
        </el-input>
      </el-form-item>
<!--      <el-form-item label="标注标签">-->
<!--        <el-tag-->
<!--          :key="tag"-->
<!--          v-for="tag in task.dynamicTags"-->
<!--          closable-->
<!--          :disable-transitions="false"-->
<!--          @close="handleClose(tag)">-->
<!--          {{tag}}-->
<!--        </el-tag>-->
<!--        <el-input-->
<!--          class="input-new-tag"-->
<!--          v-if="inputVisible"-->
<!--          v-model="inputValue"-->
<!--          ref="saveTagInput"-->
<!--          size="small"-->
<!--          @keyup.enter.native="handleInputConfirm"-->
<!--          @blur="handleInputConfirm"-->
<!--        >-->
<!--        </el-input>-->
<!--        <el-button v-else class="button-new-tag" size="small" @click="showInput">+ New Tag</el-button>-->
<!--      </el-form-item>-->
<!--      <el-form-item label="文件类型">-->
<!--        <el-radio-group v-model="task.resource">-->
<!--          <el-radio label="图片"></el-radio>-->
<!--          <el-radio label="视频"></el-radio>-->
<!--        </el-radio-group>-->
<!--      </el-form-item>-->
      <el-form-item label="任务描述">
        <el-input
          type="textarea"
          v-model="task.desc"
          class = "el-input"
        >
        </el-input>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="onSubmit">立即创建</el-button>
        <el-button>取消</el-button>
      </el-form-item>
    </el-form>
    </el-card>

    <el-card shadow="always">
      <div slot="header" class="el-card-header">
        <h2 class="login-title">上传图片</h2>
      </div>
      <el-upload
        name = 'file'
        ref="upload"
        action="http://127.0.0.1:8000/api/upload"
        :data="{username:this.username}"
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

    </el-card>
    <el-button type="primary" class="el-button" @click="submitUpload">创建</el-button>
  </div>
</template>

<script>
import Hints from '../../components/Hints'
import { selectData, cascaderData } from './data'
import axios from 'axios'
import Qs from 'qs'

export default {
  name: 'Form',
  components: { Hints },
    data() {
      return {
        username: localStorage.getItem('username'),
        task: {
          name: '',
          type: [],
          dynamicTags: ['标签一', '标签二', '标签三'],
          resource: '',
          desc: '',
        },

        inputVisible: false,
        inputValue: '',

        dialogImageUrl: '',
        dialogVisible: false,
        disabled: false,

      }
    },
    methods: {
      onSubmit() {
        console.log('submit!');
        console.log(this.username)
        // let newTask = new FormData();
        // newTask.append('name', this.task.name);
        // newTask.append('type', this.task.type);
        // newTask.append('dynamicTags', this.task.dynamicTags);
        // newTask.append('resource', this.task.resource);
        // newTask.append('imgs', this.task.imgs);
        let newTask = {
          name: '',
          type: [],
          dynamicTags: ['标签一', '标签二', '标签三'],
          resource: '',
          desc: '',
          imgs: '',
        };
        newTask.type = this.task.type;
        newTask.dynamicTags = this.task.dynamicTags;
        newTask.resource = this.task.resource;
        newTask.imgs = this.task.imgs;

        let parm = Qs.stringify({
          'username': this.username,
          'taskname': this.task.name,
          'desc': this.task.desc
        })

        axios.post('http://127.0.0.1:8000/api/createTask', parm).then(resp => {

          }
        )


        console.log(newTask);
        console.log(this.task.name)
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
      },
      handleRemove(file) {
          console.log(file);
      },
      handlePictureCardPreview(file) {
        this.dialogImageUrl = file.url;
        this.dialogVisible = true;
      },

      submitUpload() {
        console.log('submit!');
        console.log(this.username)
        // let newTask = new FormData();
        // newTask.append('name', this.task.name);
        // newTask.append('type', this.task.type);
        // newTask.append('dynamicTags', this.task.dynamicTags);
        // newTask.append('resource', this.task.resource);
        // newTask.append('imgs', this.task.imgs);
        let newTask = {
          name: '',
          type: [],
          dynamicTags: ['标签一', '标签二', '标签三'],
          resource: '',
          desc: '',
          imgs: '',
        };
        newTask.type = this.task.type;
        newTask.dynamicTags = this.task.dynamicTags;
        newTask.resource = this.task.resource;
        newTask.imgs = this.task.imgs;

        console.log(newTask);
        console.log(this.task.name)


        this.$refs.upload.submit()
      },

      handleDownload(file) {
        console.log(file);
      },
      beforeAvatarUpload(file) {
        const isJPG = file.type === 'image/jpeg';
        const isLt2M = file.size / 1024 / 1024 < 2;

        if (!isJPG) {
          this.$message.error('上传头像图片只能是 JPG 格式!');
        }
        if (!isLt2M) {
          this.$message.error('上传头像图片大小不能超过 2MB!');
        }
        return isJPG && isLt2M;
      },
      handlePreview(file) {
        console.log(file);
      }
    },
  }
</script>

<style lang="less">
.form-list-wrapper {
  .el-card{
  position: relative;
  margin-top:  10px;
  //left: 15%;
  //width: 70%;
  .el-card-header{
    height: 40px;
  }
}

  .el-card {
    padding-top: 20px;
  }
  .el-input {
    width: 80%
  }
  .el-button{
    position: relative;
    margin-top: 10px
  }

  //.form-list {
  //  width: 45%;
  //  margin: 0 auto;
  //  .el-rate {
  //    line-height: 2;
  //  }
  //  > .el-form-item {
  //    margin-bottom: 22px;
  //    .line {
  //      text-align: center;
  //    }
  //    .tip-title {
  //      text-align: right;
  //      color: #606266;
  //    }
  //  }
  //  .submit-box {
  //    margin-top: 35px;
  //    margin-left: 0;
  //    text-align: center;
  //  }
  //}
}



</style>
