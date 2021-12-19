<template>
<!--  <div class="org-tree-wrapper" :style="{ height: displayMode === 'vertical' ? '650px' : '1050px' }">-->
<!--    <Hints>-->
<!--      <template slot="hintName">树状组织图</template>-->
<!--      <template slot="hintInfo">-->
<!--        <p>v-org-tree：基于vue的树结构组织图，可用于公司组织架构展示</p>-->
<!--        <p>github地址：访问 <el-link type="success" href="https://github.com/lison16/v-org-tree" target="_blank">v-org-tree</el-link></p>-->
<!--      </template>-->
<!--    </Hints>-->
<!--    <div class="ctrl-box">-->
<!--      <div class="btn-item">-->
<!--        <span>排列方式：</span>-->
<!--        <el-radio-group v-model="displayMode" size="small">-->
<!--          <el-radio-button label="vertical">竖排</el-radio-button>-->
<!--          <el-radio-button label="horizontal">横排</el-radio-button>-->
<!--        </el-radio-group>-->
<!--      </div>-->
<!--      <div class="btn-item">-->
<!--        <span>展开全部：</span>-->
<!--        <el-switch v-model="expandAll" />-->
<!--      </div>-->
<!--    </div>-->
<!--    <div class="zoom-box">-->
<!--      <ZoomController v-model="zoom" :min="80" :max="120" :diff="10" />-->
<!--    </div>-->
<!--    <OrgView :zoom-val="zoomVal" :expand-all="expandAll" :horizontal="horizontal" />-->
<!--  </div>-->
  <div class="app-container">
    <!-- 按钮组 -->
    <div class="button-group">
      <div class="button-group-item">
        <el-upload
          class="upload-demo"
          name="file"
          multiple
          accept="text/plain"
          :headers="{ 'annotate-system-token': token }"
          action="http://localhost:8000/api/annotate_text/upload/"
          :on-success="handleSuccess"
          :on-error="handleError"
          :show-file-list="false"
        >
          <el-button type="primary">
            打开文件夹
          </el-button>
        </el-upload>
      </div>
    </div>
    <div>
      <!--  -->
      <ui-marker
        ref="aiPanel-editor"
        class="ai-observer"
                 v-bind:uniqueKey="uuid"
                 :ratio="16/9"
                 v-bind:readOnly="readOnly"
                 v-bind:imgUrl="currentImage"
      >
      </ui-marker>
    </div>
  </div>
</template>

<script>
// import OrgView from '../../components/OrgTree/OrgView'
// import ZoomController from '../../components/OrgTree/ZoomController'
// import Hints from '../../components/Hints'
import { AIMarker } from 'vue-picture-bd-marker'

export default {
  name: 'OrgTree',
  // components: { OrgView, ZoomController, Hints },
  components: { 'ui-marker': AIMarker },
  data() {
    return {
      searchTarget: '描述', // 搜索对象
      uuid: '0da9130',
      readOnly: false,
      currentImage: '../../assets/img/login-background.jpg',
      keywords: '', // 搜索关键词
      filterList: [], // 符合条件的数据
      list: [], // 所有数据列表
      listLoading: true, // 加载效果
      showEditForm: false, // 编辑框的显隐
      listEditIndex: 0, // 编辑索引
      handleItemId: 0, // 操作条目的id
      form: {
        // 编辑框数据
        description: ' ',
        text: ''
      }
    }
  },
  computed: {
    zoomVal() {
      return this.zoom / 100
    },
    horizontal() {
      if (this.displayMode === 'vertical') {
        return false
      } else {
        return true
      }
    }
  }
}
</script>

<style lang="less">
.org-tree-wrapper {
  position: relative;
  min-height: 580px;
  .ctrl-box {
    .btn-item {
      margin-bottom: 10px;
      .el-radio-button--small {
        .el-radio-button__inner {
          padding: 5px 10px;
        }
      }
    }
  }
  .zoom-box {
    position: absolute;
    bottom: 0;
    right: 25px;
  }
}
</style>
