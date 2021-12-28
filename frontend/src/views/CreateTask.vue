<template>
  <div class="form-list-wrapper">
    <Hints>
      <template slot="hintName">创建任务</template>
      <template slot="hintInfo">
        <p>创建标注任务：输入任务名称、任务描述、选择任务图片</p>
      </template>
    </Hints>
    <el-card shadow="always" class = "el-card">
      <div slot="header" class="el-card-header">
        <h2 class="login-title">任务信息</h2>
      </div>
    <el-form ref="task" :model="task" :rules="taskRules" label-width="80px">
      <el-form-item prop="name" label="任务名称">
        <el-input
          v-model="task.name"
          maxlength="10"
          show-word-limit
          class = "el-input"
        >
        </el-input>
      </el-form-item>
      <el-form-item prop="desc" label="任务描述">
        <el-input
          type="textarea"
          v-model="task.desc"
          class = "el-input"
        >
        </el-input>
      </el-form-item>
      <el-form-item label = "任务图片">
        <el-button type="text" @click="dialogTableVisible = true">请选择图片</el-button>
      </el-form-item>
      <el-form-item label = "图片预览">
          <div class = 'pic' v-for = "v in checkList">
            <img :src = "'data:img/jpg;base64,' + v.b64" alt="">
          </div>

<!--        <el-checkbox v-for="v in imglist" :label="v.filename" :key="v.filename">-->
<!--          {{v.filename}}-->
<!--          <div> <img :src = "'data:img/jpg;base64,' + v.base64" alt="" class="img"></div>-->
<!--        </el-checkbox>-->
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="onSubmit">立即创建</el-button>
        <el-button>取消</el-button>
      </el-form-item>
    </el-form>
    </el-card>
    <el-dialog title="选择图片" :visible.sync="dialogTableVisible" @click="showImg">
      <el-checkbox-group
        v-model="checkList"
      >
        <el-checkbox v-for="v in imglist" :label="v.filename" :key="v.filename">
          {{v.filename}}
          <div> <img :src = "'data:img/jpg;base64,' + v.base64" alt="" class="img"></div>
        </el-checkbox>
      </el-checkbox-group>


      <el-button type="primary" @click="selectImg">完成</el-button>


    </el-dialog>

  </div>
</template>

<script>
import Hints from '../components/Hints'
// import { selectData, cascaderData } from './data'
import axios from 'axios'
import Qs from 'qs'
import {getTaskImg} from "../api";

export default {
  name: 'Form',
  components: { Hints },
    data() {
      return {
        imglist: [],
        checkList: [],
        multipleSelection: [],
        username: localStorage.getItem('username'),
        task: {
          name: '',
          desc: '',
        },

        inputVisible: false,
        inputValue: '',

        dialogImageUrl: '',
        dialogVisible: false,

        dialogTableVisible: false,
        dialogFormVisible: false,
        formLabelWidth: '120px',

        taskRules: {
          name: [
            { required: true, trigger: 'blur', message: '请输入任务名' },
          ],
          desc: [
            { required: true, trigger: 'blur', message: '请输入任务描述' },
          ],
        }
      };
    },

    created() {
      this.showImg()
    },

    methods: {
      selectImg(){
        console.log(this.checkList)
        this.dialogTableVisible = false
      },
      showImg(){
        console.log('show')
        console.log(this.checkList)
        let parm = Qs.stringify({'username': this.username})
        let _this = this
        axios.post('http://127.0.0.1:8000/api/getTaskImg', parm).then(
          function (res) {
            console.log(res.data)
            const imgname = res.data.filename
            const imgbase = res.data.base64
            for ( let i = 0; i < res.data.filename.length; i++){
              let temp = {filename: res.data.filename[i], base64: res.data.base64[i]}
              _this.imglist.push(temp)
            }
            console.log(imgname)
        })
      },
      handleSelectionChange(val) {
        this.multipleSelection = val
      },
      onSubmit() {
        this.$refs.task.validate(valid => {
          if(valid){
         console.log('submit!');
        console.log(this.username)
        console.log(this.checkList)

        let parm = Qs.stringify({
          'username': this.username,
          'taskname': this.task.name,
          'desc': this.task.desc,
          'imglist': this.checkList
        }, {indices: false})

        axios.post('http://127.0.0.1:8000/api/createTask', parm).then(resp => {
          if(resp.data.code === 0){
            this.$message({
              message: '创建成功',
              type: 'success'
            })
          }
          else{
            this.$message.error('任务名重复，请重新输入')
          }
          }
        )
          }
        })

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
  .img{
    width: 100px;
    height: 100px;
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
