<template>
  <div class="table-classic-wrapper">
    <Hints>
      <template slot="hintName">任务列表</template>
      <template slot="hintInfo">
        <p>任务列表：显示当前所有任务及状态，可以领取任务</p>
      </template>
    </Hints>
    <el-card shadow="always" class="el-card">
      <div class="control-btns">
        <el-button type="primary" @click="createTask">创建任务</el-button>
        <el-button @click="fetchData">刷新</el-button>
      </div>
      <el-scrollbar style="height: 500px">
      <el-table
        ref="multipleTable"
        v-loading="listLoading"
        :data="tableData"
        tooltip-effect="dark"
        style="width: 100%"
        size="medium"
        @selection-change="handleSelectionChange"
      >
        <el-table-column prop="id" label="编号" align="center" width="120" sortable />
        <el-table-column prop="task_name" label="任务名" align="center">
        </el-table-column>

        <el-table-column prop="publish_user_id" label="发布者" align="center" />
        <el-table-column label="任务描述" align="center">
          <template slot-scope="scope">
          <el-button size="mini" :disabled="scope.row.forbid" @click="handleEdit(scope.$index, scope.row)">查看</el-button>
          </template>
        </el-table-column>


        <el-table-column prop="status" label="任务状态" align="center" />
        <el-table-column prop="claim_user_id" label="领取者" align="center" />

        <el-table-column label="操作" align="center" width="200">
          <template slot-scope="scope">

            <el-button type='primary' @click="claimTask(scope.$index, scope.row)">领取</el-button>
          </template>
        </el-table-column>
      </el-table>
        </el-scrollbar>
      <!-- 新增/编辑 弹出栏 -->
      <el-dialog
        title="任务描述"
        :visible.sync="formVisible"
        width="30%"
        class="dialog-form"
        :before-close="handleClose"
      >
        <el-form
          ref="dialogForm"
          :model="dialogForm"
          :rules="formRules"
          label-width="100px"
        >
            <el-input :placeholder="dialogForm.desc"  :disabled="true" />
        </el-form>
      </el-dialog>
    </el-card>
  </div>
</template>

<script>
import { getTableList } from '../api'
import excel from '../utils/excel'
import Pagination from '../components/Pagination'
import Upload from '../components/Upload'
import Hints from '../components/Hints'
import Qs from "qs";
import axios from "axios";


export default {
  name: 'Table',
  components: { Pagination, Upload, Hints },
  data() {
    return {
      // 数据列表加载动画
      username: localStorage.getItem('username'),
      listLoading: true,
      // 查询列表参数对象
      listQuery: {
        id: undefined,
        phone: undefined,
        married: undefined,
        currentPage: 1,
        pageSize: 10
      },
      // 新增/编辑提交表单对象
      dialogForm: {
        desc: undefined
        // name: undefined,
        // phone: undefined,
        // married: undefined,
        // hobby: []
      },
      // 数据总条数
      total: 0,
      // 表格数据数组
      tableData: [],
      // 多选数据暂存数组
      multipleSelection: [],
      // 新增/编辑 弹出框显示/隐藏
      formVisible: false,
      // 表单校验 trigger: ['blur', 'change'] 为多个事件触发
      formRules: {
        name: [
          { required: true, message: '请输入姓名', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入手机号', trigger: 'blur' },
          { pattern: /^1[3456789]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
        ]
      },
      // 防止多次连续提交表单
      isSubmit: false,
      // 导入数据 弹出框显示/隐藏
    }
  },
  created() {
    this.fetchData()
  },
  mounted(){
    this.fetchData()
  },
  methods: {
    handleEdit(index, row) {
      console.log(index, row)
      this.formVisible = true
      this.dialogForm.name = row.name
      this.dialogForm.desc = row.description
    },
    // 获取数据列表
    fetchData() {
      this.listLoading = true
      // 获取数据列表接口
      let username = localStorage.getItem('username')
      console.log(username)

      let parm = Qs.stringify({'user_name': localStorage.getItem('username')})

      console.log(parm)


      getTableList(Qs.stringify({'username': localStorage.getItem('username')})).then(res => {
        const data = res.data
        console.log(data)
        if (data.code === 0) {
          // this.total = data.data.total
          this.tableData = data.data
          this.listLoading = false
        }
      }).catch(() => {
        this.listLoading = false
      })
    },
    claimTask(index, row){
      var parm = Qs.stringify({
        'username': this.username,
        'taskname': row.task_name,
      })
      console.log('claim')
      console.log(this.username)
      console.log(parm)
      axios.post('http://127.0.0.1:8000/api/claimTask', parm).then(res => {

      })
      this.fetchData()
    },

    // 查询数据
    onSubmit() {
      this.listQuery.currentPage = 1
      this.fetchData()
    },
    // 导入数据
    handleImport() {
      this.importVisible = true
    },
    // 新增/编辑表单确认提交
    submitForm(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          // 此处添加 新增/编辑数据的接口 新增成功后调用fetchData方法更新列表
          // 先 this.isSubmit = true 接口返回成功后 再 this.isSubmit = false
          this.formVisible = false
        } else {
          this.isSubmit = false
          return false
        }
      })
    },
    // 新增/编辑表单取消提交
    cancleForm() {
      this.$refs.dialogForm.resetFields()
      this.formVisible = false
    },
    // 导入数据弹出栏 确认操作
    confirmImport() {
      // 此处添加 后台接收的接口，将导入的数据传给后台处理
      this.importVisible = false
    },
    // 导入数据弹出栏 取消操作
    cancleImport() {
      // 将导入的数据清空
      this.importVisible = false
    },
    // 导出数据--excle格式
    exportTable(type) {
      if (this.tableData.length) {
        const params = {
          header: ['编号', '姓名', '性别', '手机', '学历', '婚姻状况', '禁止编辑', '爱好'],
          key: ['id', 'user_id', 'sex', 'phone', 'education', 'married', 'forbid', 'hobby'],
          data: this.tableData,
          autoWidth: true,
          fileName: '综合表格',
          bookType: type
        }
        excel.exportDataToExcel(params)
        this.exportVisible = false
      }
    },
    createTask(){
      this.$router.push('/createTask')
    }
  }
}
</script>

<style lang="less">
.table-classic-wrapper {
  .el-card {
    min-height: 656px;
  }
  .control-btns {
    margin-bottom: 20px;
  }
  .search-form {
    padding-top: 18px;
    margin-bottom: 15px;
    background-color: #f7f8fb;
  }
  .el-table thead {
    font-weight: 600;
    th {
      background-color: #f2f3f7;
    }
  }
  .dialog-form {
    .el-input {
      width: 380px;
    }
    .footer-item {
      margin-top: 50px;
      text-align: right;
    }
  }
  .upload-box,
  .export-data {
    width: 300px;
    margin: 0 auto 30px;
  }
  .upload-box {
    width: 156px;
    .files-upload {
      color: #20a0ff;
    }
  }
  .hints {
    font-size: 12px;
    color: #aaa;
    text-align: center;
  }
  .el-card{
    height: 400px;
  }
}
</style>
