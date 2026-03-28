<template>
	<div :style='{"width":"1200px","padding":"0px","margin":"20px auto","position":"relative","background":"rgb(255, 255, 255)"}'>
		<div class="section-title" :style='{"margin":"10px 0","color":"#333","textAlign":"center","background":"#f7db61","width":"100%","fontSize":"24px","lineHeight":"50px","border-bottom":"1px solid #1f292f"}'>在线交流</div>
		<div class="back_box">
			<el-button class="backBtn" size="mini" @click="backClick">
				<span class="icon iconfont icon-jiantou33"></span>
				<span>返回</span>
			</el-button>
		</div>
		<el-form class="add-update-preview" :model="form" :rules="rules" ref="form" label-width="180px">
			<el-form-item :style='{"border":"2px inset #f7db6150","padding":"10px","margin":"0 0 10px","background":"#f7db6110"}' label="标题" prop="title">
				<el-input v-model="form.title" placeholder="请输入标题"></el-input>
			</el-form-item>
			<el-form-item :style='{"border":"2px inset #f7db6150","padding":"10px","margin":"0 0 10px","background":"#f7db6110"}' label="分类" prop="typename">
				<el-select v-model="form.typename" placeholder="请选择分类">
					<el-option
						v-for="(item,index) in categoryList"
						:key="index"
						:label="item.typename"
						:value="item.typename">
					</el-option>
				</el-select>
			</el-form-item>
			<el-form-item :style='{"border":"2px inset #f7db6150","padding":"10px","margin":"0 0 10px","background":"#f7db6110"}' label="封面图" prop="cover">
				<file-upload
					tip="点击上传封面图"
					action="file/upload"
					:limit="3"
					:multiple="true"
					:fileUrls="form.cover?form.cover:''"
					@change="coverUploadChange"
					></file-upload>
			</el-form-item>
			<el-form-item :style='{"border":"2px inset #f7db6150","padding":"10px","margin":"0 0 10px","background":"#f7db6110"}' label="类型" prop="isdone">
				<el-radio-group v-model="form.isdone">
					<el-radio label="开放">公开</el-radio>
					<el-radio label="关闭">私人</el-radio>
				</el-radio-group>
			</el-form-item>
			<el-form-item :style='{"border":"2px inset #f7db6150","padding":"10px","margin":"0 0 10px","background":"#f7db6110"}' label="是否匿名" prop="isanon">
				<el-radio-group v-model="form.isanon">
					<el-radio :label="1">是</el-radio>
					<el-radio :label="0">否</el-radio>
				</el-radio-group>
			</el-form-item>
			<el-form-item :style='{"border":"2px inset #f7db6150","padding":"10px","margin":"0 0 10px","background":"#f7db6110"}' label="内容" prop="content">
				<editor
					:style='{"minHeight":"350px","border":"1px solid #ccc","boxShadow":"0 0 0px rgba(80, 80, 80, .2)","color":"#333","borderRadius":"4px","width":"100%","lineHeight":"32px","fontSize":"14px"}'
					v-model="form.content" 
					class="editor" 
					action="file/upload">
				</editor>
			</el-form-item>
			<el-form-item :style='{"padding":"0","margin":"20px 0"}'>
				<el-button :style='{"border":"0","cursor":"pointer","padding":"0 15px","margin":"0 20px 0 0","borderRadius":"2px","background":"#f7db61","display":"inline-block","width":"auto","lineHeight":"40px","fontSize":"16px","height":"40px"}' type="primary" @click="submitForm('form')">
					<span class="icon iconfont icon-kaitongfuwu" :style='{"color":"#333"}'></span>
					<span class="text" :style='{"color":"#333"}'>{{this.isEdit ? '修改' : '发布帖子'}}</span>
				</el-button>
				<el-button :style='{"border":"1px solid #ddd","cursor":"pointer","padding":"0 15px","margin":"0 20px 0 0","borderRadius":"2px","background":"#fff","display":"inline-block","width":"auto","lineHeight":"40px","fontSize":"16px","height":"40px"}' @click="resetForm('form')">
					<span class="icon iconfont icon-shanchu1" :style='{"color":"#666"}'></span>
					<span class="text" :style='{"color":"#666"}'>重置</span>
				</el-button>
			</el-form-item>
		</el-form>
	</div>
</template>

<script>
	export default {
		//数据集合
		data() {
			return {
				form: {
					title: '',
					isdone: '开放',
					content: '',
					parentid: 0,
					userid: localStorage.getItem('frontUserid'),
					username: localStorage.getItem('username'),
					toptime: '',
					cover: '',
					isanon: 0
				},
				editorOption: {
					modules: {
						toolbar: [
							["bold", "italic", "underline", "strike"],
							["blockquote", "code-block"],
							[{ header: 1 }, { header: 2 }],
							[{ list: "ordered" }, { list: "bullet" }],
							[{ script: "sub" }, { script: "super" }],
							[{ indent: "-1" }, { indent: "+1" }],
							[{ direction: "rtl" }],
							[{ size: ["small", false, "large", "huge"] }],
							[{ header: [1, 2, 3, 4, 5, 6, false] }],
							[{ color: [] }, { background: [] }],
							[{ font: [] }],
							[{ align: [] }],
							["clean"],
							["image", "video"]
						]
					}
				},
				isEdit: false,
				rules: {
					title: [
						{ required: true, message: '请输入标题', trigger: 'blur' }
					],
					typename: [
						{ required: true, message: '请选择分类', trigger: 'blur' }
					]
				},
				categoryList: [],
			}
		},
		created() {
			this.getCategoryList()
			if (this.$route.query.id != undefined) {
				this.isEdit = true;
				this.$http.get('forum/detail/' + this.$route.query.id,{}).then(res=>{
					if(res.data.code==0){
						this.form = res.data.data
					}
				})
			}
		},
		//方法集合
		methods: {
			getCategoryList(){
				this.$http.get('forumtype/list', {}).then(res => {
					if (res.data.code == 0) {
						this.categoryList = res.data.data.list
					}
				});
			},
			// 返回按钮
			backClick(){
				history.back()
			},
			onEditorReady(editor) {
				editor.root.setAttribute('data-placeholder', "请输入内容...");
			},
			coverUploadChange(fileUrls) {
				this.form.cover = fileUrls.replace(new RegExp(this.$config.baseUrl,"g"),"");
			},
			submitForm(formName) {
				this.$refs[formName].validate((valid) => {
					if (valid) {
						if(!this.isEdit){
							this.form.toptime = this.getCurDateTime()
						}
						if(this.form.cover==''){
							this.$message.error('请上传封面图')
							return false
						}
						this.$http.post(`forum/${this.isEdit ? 'update' : 'add'}`, this.form).then(res => {
							if (res.data.code === 0) {
								this.$message({
									message: `${this.isEdit ? '修改' : '发布'}成功`,
									type: 'success',
									duration: 1500,
									onClose: () => {
										if (this.isEdit) {
											this.$router.push('/index/myForumList');
										} else {
											this.$router.push('/index/forum');
										}
									}
								});
							} else {
								this.$message.error(res.data.msg);
							}
						});
					} else {
						return false;
					}
				});
			},
			resetForm(formName) {
				this.$refs[formName].resetFields();
			}
		}
	}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
	.add-update-preview .el-form-item /deep/ .el-form-item__label {
		padding: 0 10px 0 0;
		color: #666;
		font-weight: 500;
		width: 180px;
		font-size: inherit;
		line-height: 40px;
		text-align: right;
	}
	.add-update-preview .el-form-item /deep/ .el-form-item__content {
		margin-left: 180px;
	}
	.add-update-preview .el-input /deep/ .el-input__inner {
		border: 1px solid #ddd;
		border-radius: 0px;
		padding: 0 12px;
		box-shadow: none;
		color: inherit;
		width: auto;
		font-size: 16px;
		height: 40px;
	}
	.add-update-preview .el-select /deep/ .el-input__inner {
		border: 1px solid #ddd;
		border-radius: 0px;
		padding: 0 10px;
		color: inherit;
		width: 100%;
		font-size: 16px;
		min-width: inherit !important;
		height: 40px;
	}
  
	.add-update-preview .el-date-editor /deep/ .el-input__inner {
		border: 1px solid #ddd;
		border-radius: 0px;
		padding: 0 10px 0 30px;
		box-shadow: none;
		color: inherit;
		width: auto;
		font-size: 16px;
		height: 40px;
	}
  
	.add-update-preview /deep/ .el-upload--picture-card {
		background: transparent;
		border: 0;
		border-radius: 0;
		width: auto;
		height: auto;
		line-height: initial;
		vertical-align: middle;
	}
  
	.add-update-preview /deep/ .upload .upload-img {
		border: 1px solid #ddd;
		cursor: pointer;
		border-radius: 0px;
		color: #999;
		background: #fff;
		width: 80px;
		font-size: 26px;
		line-height: 60px;
		text-align: center;
		height: 60px;
	}
  
	.add-update-preview /deep/ .el-upload-list .el-upload-list__item {
		border: 1px solid #ddd;
		cursor: pointer;
		border-radius: 0px;
		color: #999;
		background: #fff;
		width: 80px;
		font-size: 26px;
		line-height: 60px;
		text-align: center;
		height: 60px;
	}
  
	.add-update-preview /deep/ .el-upload .el-icon-plus {
		border: 1px solid #ddd;
		cursor: pointer;
		border-radius: 0px;
		color: #999;
		background: #fff;
		width: 80px;
		font-size: 26px;
		line-height: 60px;
		text-align: center;
		height: 60px;
	}
	.add-update-preview /deep/ .el-upload__tip {
		color: #888;
		font-size: 16px;
	}
  
	.add-update-preview .el-textarea /deep/ .el-textarea__inner {
		border: 1px solid #ddd;
		border-radius: 0px;
		padding: 12px;
		box-shadow: none;
		color: inherit;
		width: auto;
		font-size: 16px;
		min-height: 150px;
		min-width: 48%;
		height: auto;
	}
</style>
