<template>
    <div id="useraccessmysql" class="useraccessmysql">
        
        <div v-if="!isapply" class="useraccessmysql-list">
            <el-row style="padding-bottom:5px;">
                <div class="user-operation">
                    <el-button @click="applyData" style="float: left;" icon="el-icon-edit" size="small" type="primary">申请权限</el-button>
                    <el-input v-model="searchcontent" @keyup.enter.native="searchData" style="width: 200px;float: right;" size="small" placeholder="Search">
                        <el-button @click="searchData" slot="append" icon="el-icon-search"></el-button>
                    </el-input>
                </div>
            </el-row>
            <el-row>
                <UserAccessTable
                :TableColumn="table_columns"
                :TableData="table_data"
                :editData="editData"
                :delData="delData">
                </UserAccessTable>
            </el-row>
        </div>
        <div v-if="isapply" class="useraccessmysql-apply">
            <el-row>
                <div style="padding-top: 10px;">
                    <el-form  ref="form" :model="form" :rules="rules">
                        <el-form-item label="申请用户：" label-width="150px" prop="username">
                            <el-input style="width: 300px; float: left;" v-model="form.username"></el-input>
                        </el-form-item>
                        <el-form-item label="申请访问实例：" label-width="150px" prop="mysqlinst">
                            <el-select style="width: 300px; float: left;" v-model="form.mysqlinst" @change="getInstDb($event)" placeholder="请选择MySQL实例">
                                <el-option v-for="(val,index) in instlist" :key="index" :label="val.inst" :value="val.id" ></el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item  label="申请访问数据库：" label-width="150px" prop="user_access_db">
                            <el-checkbox-group style="float: left;" v-model="form.user_access_db">
                                <el-checkbox v-for="(val,index) in instdb" :key="index" :label="val"></el-checkbox>
                            </el-checkbox-group>
                        </el-form-item>
                        <el-form-item label="申请说明：" label-width="150px">
                            <el-input style="width: 300px; float: left;" v-model="form.comment"></el-input>
                        </el-form-item>
                        <el-form-item label-width="150px">
                            <el-button style="float: left;" type="primary" @click="handleApply">提交</el-button>
                            <el-button style="float: left;" @click="isapply = false;">取消</el-button>
                        </el-form-item>
                    </el-form>
                </div>
            </el-row>
            
        </div>
    </div>
</template>

<script>
import store from '@/store/store.js';
import UserAccessTable from './UserAccessTable.vue';
import { getUserAccessMysql,getMysqlInst,getMysqlMeta,editUserAccessMysql,delUserAccessMysql,addUserAccessMysql,searchUserAccessMysql } from '@/api/db.js';
export default {
    name: "useraccessmysql",
    components: {
        UserAccessTable,
    },
    data () {
        return {
            searchcontent: '',
            //用户列表参数
            table_data: [],
            table_columns: {
                id: 'id',
                username: '用户名',
                mysqlinst: 'MySQL实例',
                user_access_db: '访问数据库',
                create_time: '申请时间',
                status: '状态',
                comment: '备注'
            },
            //用户申请相关参数
            instlist: [],
            instdb: [],
            form: {
                username: '',
                mysqlinst: '',
                user_access_db: [],
                comment: '',
            },
            rules: {
                username: [
                    { required: true, message: '请输入用户名', trigger: 'blur' }
                ],
                mysqlinst: [
                    { required: true, message: '请选择MySQL实例', trigger: 'change' }
                ],
                user_access_db: [
                    { type: 'array',required: true, message: '请至少选择一个MySQL数据库', trigger: 'change' }
                ],
            },
            isapply: false,
        }
    },
    methods: {
        applyData() {
            this.isapply = true
        },
        handleApply() {
            this.$refs['form'].validate((valid)=>{
                if(valid){
                    addUserAccessMysql(this.form).then((response) => {
                        if (response) {
                            this.$message.success('申请成功!');
                            this.getDataList()
                            this.isapply = false;
                        }
                    }).catch((error) => {
                        this.$message.error('申请失败，请确认是否重复申请!');
                        console.log('error!');
                    })
                }
                else {
                    this.$message.error('数据不合法!');
                }
            })
        },
        delData(id) {
            delUserAccessMysql({id:id}).then((response) => {
                // console.log(response);
                this.$message.success('删除成功!');
            }).catch((error) => {
                console.log(error);
            })
        },
        editData (data) {
            editUserAccessMysql(data).then((response) => {
                this.$message.success('处理成功!');
            }).catch((error) => {
                console.log(error);
            })
        },
        searchData() {
            if (this.searchcontent) {
                searchUserAccessMysql({searchcontent:this.searchcontent}).then((response) => {
                    this.table_data = response.data
                }).catch((error) => {
                    console.log(error);
                })
            }
            else {
                this.getDataList()
            }
        },
        getDataList() {
            getUserAccessMysql({'username':store.getters.username}).then((response) => {
                this.table_data = response.data
            }).catch((error) => {
                console.log(error);
            })
        },
        getMysqlInst() {
            getMysqlInst().then((response) => {
                if (response.data.length > 0) {
                    if (store.getters.userissuper) {
                        for (var i = 0; i < response.data.length;i++) {
                            this.instlist.push({'id':response.data[i].id,'inst':response.data[i].inst_name})
                        }
                    }
                    else {
                        for (var i = 0; i < response.data.length;i++) {
                            if (response.data[i].role == 'Slave' ) {
                                this.instlist.push({'id':response.data[i].id,'inst':response.data[i].inst_name})  
                            }
                        }
                    }
                }
            }).catch((error) => {
                console.log(error);
            })
        },
        getInstDb (val) {
            this.instdb = []
            let req_data = {}
            req_data.type = 'database'
            req_data.instid = val
            getMysqlMeta(req_data).then((response) => {
                for (let i=0;i<response.data.results.length;i++) {
                    this.instdb.push(response.data.results[i].table_schema)
                }
                this.form.user_access_db = []
            }).catch((error) => {
                console.log(error);
            })
            
        },
        initUserApplyData() {
            this.form.username = store.getters.username
        },
    },
    mounted() {
        this.getDataList()
        this.getMysqlInst()
        this.initUserApplyData()
    },

}
</script>


<style>
.useraccessmysql .el-collapse-item__header.is-active,.useraccessmysql .el-collapse-item__header{
    font-size: 16px;
    font-weight: bold;
    padding-left: 0.5em;
    border-bottom: 1px solid #dcdfe6;
}
</style>
