<template>
  <div class="home-wrapper">
    <el-card shadow="always" :body-style="{padding: '0px'}" class="card">
        <img src="../assets/img/Home.png" alt="icon" class="img">
    </el-card>

    <div class="date-row">
      <div class="data-col">
        <el-card shadow="always" :body-style="{padding: '0px'}" @click.native="goTasklist">
          <div class="date-block">
            <i :class="'vue-dsn-icon-wendang'" :style="{ background: '#2d8cf0' }" class="icon-box" />
            <div class="date-cont">
              <p class="title">任务列表</p>
            </div>
          </div>
        </el-card>
      </div>
      <div class="data-col">
        <el-card shadow="always" :body-style="{padding: '0px'}" @click.native="goUploadImg">
          <div class="date-block">
            <i :class="'vue-dsn-icon-picture'" :style="{ background: '#19be6b' }" class="icon-box" />
            <div class="date-cont">
              <p class="title">图片上传</p>
            </div>
          </div>
        </el-card>
      </div>
      <div class="data-col">
        <el-card shadow="always" :body-style="{padding: '0px'}" @click.native="goUploadVideo">
          <div class="date-block">
            <i :class="'vue-dsn-icon-video'" :style="{ background: '#ff9900' }" class="icon-box" />
            <div class="date-cont">
              <p class="title">视频上传</p>
            </div>
          </div>
        </el-card>
      </div>
      <div class="data-col">
        <el-card shadow="always" :body-style="{padding: '0px'}" @click.native="goTaskCreate">
          <div class="date-block">
            <i :class="'vue-dsn-icon-biaoge'" :style="{ background: '#e46cbb' }" class="icon-box" />
            <div class="date-cont">
              <p class="title">任务创建</p>
            </div>
          </div>
        </el-card>
      </div>
      <div class="data-col">
        <el-card shadow="always" :body-style="{padding: '0px'}" @click.native="goImgLabel">
          <div class="date-block">
            <i :class="'vue-dsn-icon-bianjiqi'" :style="{ background: '#9a66e4' }" class="icon-box" />
            <div class="date-cont">
              <p class="title">图片标注</p>
            </div>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script>
import CountTo from 'vue-count-to'
import ChartsPie from '../components/Charts/ChartsPie'
import ChartsBar from '../components/Charts/ChartsBar'
import ChartsLine from '../components/Charts/ChartsLine'
export default {
  name: 'Home',
  components: { CountTo, ChartsPie, ChartsBar, ChartsLine },
  data() {
    return {
    }
  },
  methods: {
    goTasklist() {
      this.$router.push('/tasklist');
    },
    goUploadImg() {
      this.$router.push('/uploadImg');
    },
    goUploadVideo() {
      this.$router.push('/uploadVideo');
    },
    goTaskCreate() {
      this.$router.push('/createTask');
    },
    goImgLabel() {
      this.$router.push('/imgLabel');
    },
  }
}
</script>

<style lang="less">
.home-wrapper{
  .img{
    height: 200px;
    display: flex;
    margin-top: 50px
  }
  .date-row{
    margin-top: 30px;
    width: 100%;
    display: flex;
    margin-bottom: 20px;
    .data-col{
      flex: 1;
      margin-right: 20px;
      &:last-child{
        margin-right: 0;
      }
      .date-block{
        display: flex;
        align-items: center;
        height: 120px;
        .icon-box{
          font-size: 40px;
          width: 120px;
          height: 120px;
          text-align: center;
          line-height: 120px;
          color: #fff;
        }
        .date-cont{
          flex: 1;
          text-align: center;
          color: #515a6e;
          .count{
            line-height: 60px;
            font-size: 35px;
          }
          .title{
            font-size: 16px;
          }
        }
      }
    }
  }
  .card{
    height: 350px;
  }
}
</style>
