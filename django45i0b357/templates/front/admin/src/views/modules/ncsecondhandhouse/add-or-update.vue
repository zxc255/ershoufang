<template>
	<div class="addEdit-block">
		<el-form
			class="add-update-preview"
			ref="ruleForm"
			:model="ruleForm"
			:rules="rules"
			label-width="180px"
		>
			<template >
				<el-form-item class="input" v-if="type!='info'"  label="朝向" prop="orientation" >
					<el-input v-model="ruleForm.orientation" placeholder="朝向" clearable  :readonly="ro.orientation"></el-input>
				</el-form-item>
				<el-form-item v-else class="input" label="朝向" prop="orientation" >
					<el-input v-model="ruleForm.orientation" placeholder="朝向" readonly></el-input>
				</el-form-item>
				<el-form-item class="input" v-if="type!='info'"  label="装修" prop="fitment" >
					<el-input v-model="ruleForm.fitment" placeholder="装修" clearable  :readonly="ro.fitment"></el-input>
				</el-form-item>
				<el-form-item v-else class="input" label="装修" prop="fitment" >
					<el-input v-model="ruleForm.fitment" placeholder="装修" readonly></el-input>
				</el-form-item>
				<el-form-item class="input" v-if="type!='info'"  label="面积" prop="area" >
					<el-input v-model="ruleForm.area" placeholder="面积" clearable  :readonly="ro.area"></el-input>
				</el-form-item>
				<el-form-item v-else class="input" label="面积" prop="area" >
					<el-input v-model="ruleForm.area" placeholder="面积" readonly></el-input>
				</el-form-item>
				<el-form-item class="input" v-if="type!='info'"  label="竣工" prop="becompleted" >
					<el-input v-model="ruleForm.becompleted" placeholder="竣工" clearable  :readonly="ro.becompleted"></el-input>
				</el-form-item>
				<el-form-item v-else class="input" label="竣工" prop="becompleted" >
					<el-input v-model="ruleForm.becompleted" placeholder="竣工" readonly></el-input>
				</el-form-item>
				<el-form-item class="input" v-if="type!='info'"  label="小区" prop="plot" >
					<el-input v-model="ruleForm.plot" placeholder="小区" clearable  :readonly="ro.plot"></el-input>
				</el-form-item>
				<el-form-item v-else class="input" label="小区" prop="plot" >
					<el-input v-model="ruleForm.plot" placeholder="小区" readonly></el-input>
				</el-form-item>
				<el-form-item class="input" v-if="type!='info'"  label="区域" prop="region" >
					<el-input v-model="ruleForm.region" placeholder="区域" clearable  :readonly="ro.region"></el-input>
				</el-form-item>
				<el-form-item v-else class="input" label="区域" prop="region" >
					<el-input v-model="ruleForm.region" placeholder="区域" readonly></el-input>
				</el-form-item>
				<el-form-item class="upload" v-if="type!='info' && !ro.cover" label="封面" prop="cover" >
					<file-upload
						tip="点击上传封面"
						action="file/upload"
						:limit="3"
						:multiple="true"
						:fileUrls="ruleForm.cover?ruleForm.cover:''"
						@change="coverUploadChange"
					></file-upload>
				</el-form-item>
				<el-form-item class="upload" v-else-if="ruleForm.cover" label="封面" prop="cover" >
					<img v-if="ruleForm.cover.substring(0,4)=='http'" class="upload-img" style="margin-right:20px;" v-bind:key="index" :src="ruleForm.cover.split(',')[0]" width="100" height="100">
					<img v-else class="upload-img" style="margin-right:20px;" v-bind:key="index" v-for="(item,index) in ruleForm.cover.split(',')" :src="$base.url+item" width="100" height="100">
				</el-form-item>
				<el-form-item class="input" v-if="type!='info'"  label="标题" prop="title" >
					<el-input v-model="ruleForm.title" placeholder="标题" clearable  :readonly="ro.title"></el-input>
				</el-form-item>
				<el-form-item v-else class="input" label="标题" prop="title" >
					<el-input v-model="ruleForm.title" placeholder="标题" readonly></el-input>
				</el-form-item>
				<el-form-item class="input" v-if="type!='info'"  label="总价(万)" prop="totalprice" >
					<el-input-number v-model="ruleForm.totalprice" placeholder="总价(万)" :disabled="ro.totalprice"></el-input-number>
				</el-form-item>
				<el-form-item v-else class="input" label="总价(万)" prop="totalprice" >
					<el-input v-model="ruleForm.totalprice" placeholder="总价(万)" readonly></el-input>
				</el-form-item>
				<el-form-item class="input" v-if="type!='info'"  label="单价" prop="unitprice" >
					<el-input-number v-model="ruleForm.unitprice" placeholder="单价" :disabled="ro.unitprice"></el-input-number>
				</el-form-item>
				<el-form-item v-else class="input" label="单价" prop="unitprice" >
					<el-input v-model="ruleForm.unitprice" placeholder="单价" readonly></el-input>
				</el-form-item>
				<el-form-item class="input" v-if="type!='info'"  label="户型" prop="types" >
					<el-input v-model="ruleForm.types" placeholder="户型" clearable  :readonly="ro.types"></el-input>
				</el-form-item>
				<el-form-item v-else class="input" label="户型" prop="types" >
					<el-input v-model="ruleForm.types" placeholder="户型" readonly></el-input>
				</el-form-item>
				<el-form-item class="input" v-if="type!='info'"  label="楼层" prop="floor" >
					<el-input v-model="ruleForm.floor" placeholder="楼层" clearable  :readonly="ro.floor"></el-input>
				</el-form-item>
				<el-form-item v-else class="input" label="楼层" prop="floor" >
					<el-input v-model="ruleForm.floor" placeholder="楼层" readonly></el-input>
				</el-form-item>
			</template>
			<el-form-item class="textarea" v-if="type!='info'" label="来源" prop="laiyuan" >
				<el-input
					style="min-width: 200px; max-width: 600px;"
					type="textarea"
					:rows="8"
					placeholder="来源"
					v-model="ruleForm.laiyuan" >
				</el-input>
			</el-form-item>
			<el-form-item v-else-if="ruleForm.laiyuan" label="来源" prop="laiyuan" >
				<span class="text">{{ruleForm.laiyuan}}</span>
			</el-form-item>
			<el-form-item class="btn">
				<el-button class="btn3"  v-if="type!='info'" type="success" @click="onSubmit">
					<span class="icon iconfont icon-xihuan"></span>
					提交
				</el-button>
				<el-button class="btn4" v-if="type!='info'" type="success" @click="back()">
					<span class="icon iconfont icon-xihuan"></span>
					取消
				</el-button>
				<el-button class="btn5" v-if="type=='info'" type="success" @click="back()">
					<span class="icon iconfont icon-xihuan"></span>
					返回
				</el-button>
			</el-form-item>
		</el-form>
    

	</div>
</template>
<script>
	import { 
		isNumber,
	} from "@/utils/validate";
	export default {
		data() {
			var validateNumber = (rule, value, callback) => {
				if(!value){
					callback();
				} else if (!isNumber(value)) {
					callback(new Error("请输入数字"));
				} else {
					callback();
				}
			};
			return {
				id: '',
				type: '',
			
			
				ro:{
					orientation : false,
					fitment : false,
					area : false,
					becompleted : false,
					plot : false,
					region : false,
					cover : false,
					laiyuan : false,
					title : false,
					totalprice : false,
					unitprice : false,
					types : false,
					floor : false,
				},
			
				ruleForm: {
					orientation: '',
					fitment: '',
					area: '',
					becompleted: '',
					plot: '',
					region: '',
					cover: '',
					laiyuan: '',
					title: '',
					totalprice: '',
					unitprice: '',
					types: '',
					floor: '',
				},
		

				rules: {
					orientation: [
					],
					fitment: [
					],
					area: [
					],
					becompleted: [
					],
					plot: [
					],
					region: [
					],
					cover: [
					],
					laiyuan: [
					],
					title: [
					],
					totalprice: [
						{ validator: validateNumber, trigger: 'blur' },
					],
					unitprice: [
						{ validator: validateNumber, trigger: 'blur' },
					],
					types: [
					],
					floor: [
					],
				},
			};
		},
		props: ["parent"],
		computed: {



		},
		components: {
		},
		created() {
		},
		methods: {
			// 下载
			download(file){
				window.open(`${file}`)
			},
			// 初始化
			init(id,type) {
				if (id) {
					this.id = id;
					this.type = type;
				}
				if(this.type=='info'||this.type=='else'){
					this.info(id);
				}else if(this.type=='logistics'){
					this.logistics=false;
					this.info(id);
				}else if(this.type=='cross'){
					var obj = this.$storage.getObj('crossObj');
					for (var o in obj){
						if(o=='orientation'){
							this.ruleForm.orientation = obj[o];
							this.ro.orientation = true;
							continue;
						}
						if(o=='fitment'){
							this.ruleForm.fitment = obj[o];
							this.ro.fitment = true;
							continue;
						}
						if(o=='area'){
							this.ruleForm.area = obj[o];
							this.ro.area = true;
							continue;
						}
						if(o=='becompleted'){
							this.ruleForm.becompleted = obj[o];
							this.ro.becompleted = true;
							continue;
						}
						if(o=='plot'){
							this.ruleForm.plot = obj[o];
							this.ro.plot = true;
							continue;
						}
						if(o=='region'){
							this.ruleForm.region = obj[o];
							this.ro.region = true;
							continue;
						}
						if(o=='cover'){
							this.ruleForm.cover = obj[o];
							this.ro.cover = true;
							continue;
						}
						if(o=='laiyuan'){
							this.ruleForm.laiyuan = obj[o];
							this.ro.laiyuan = true;
							continue;
						}
						if(o=='title'){
							this.ruleForm.title = obj[o];
							this.ro.title = true;
							continue;
						}
						if(o=='totalprice'){
							this.ruleForm.totalprice = obj[o];
							this.ro.totalprice = true;
							continue;
						}
						if(o=='unitprice'){
							this.ruleForm.unitprice = obj[o];
							this.ro.unitprice = true;
							continue;
						}
						if(o=='types'){
							this.ruleForm.types = obj[o];
							this.ro.types = true;
							continue;
						}
						if(o=='floor'){
							this.ruleForm.floor = obj[o];
							this.ro.floor = true;
							continue;
						}
					}
				}
			
			},
			// 多级联动参数

			info(id) {
				this.$http({
					url: `ncsecondhandhouse/info/${id}`,
					method: "get"
				}).then(({ data }) => {
					if (data && data.code === 0) {
						this.ruleForm = data.data;
						//解决前台上传图片后台不显示的问题
						let reg=new RegExp('../../../upload','g')//g代表全部
					} else {
						this.$message.error(data.msg);
					}
				});
			},

			// 提交
			async onSubmit() {
					if(this.ruleForm.cover!=null) {
						this.ruleForm.cover = this.ruleForm.cover.replace(new RegExp(this.$base.url,"g"),"");
					}
var objcross = this.$storage.getObj('crossObj');
					await this.$refs["ruleForm"].validate(async valid => {
						if (valid) {
							if(this.type=='cross'){
								var statusColumnName = this.$storage.get('statusColumnName');
								var statusColumnValue = this.$storage.get('statusColumnValue');
								if(statusColumnName!='') {
									var obj = this.$storage.getObj('crossObj');
									if(statusColumnName && !statusColumnName.startsWith("[")) {
										for (var o in obj){
											if(o==statusColumnName){
												obj[o] = statusColumnValue;
											}
										}
										var table = this.$storage.get('crossTable');
										await this.$http({
											url: `${table}/update`,
											method: "post",
											data: obj
										}).then(({ data }) => {});
									}
								}
							}
							
							await this.$http({
								url: `ncsecondhandhouse/${!this.ruleForm.id ? "save" : "update"}`,
								method: "post",
								data: this.ruleForm
							}).then(async ({ data }) => {
								if (data && data.code === 0) {
									this.$message({
										message: "操作成功",
										type: "success",
										duration: 1500,
										onClose: () => {
											this.parent.showFlag = true;
											this.parent.addOrUpdateFlag = false;
											this.parent.ncsecondhandhouseCrossAddOrUpdateFlag = false;
											this.parent.search();
											this.parent.contentStyleChange();
										}
									});
								} else {
									this.$message.error(data.msg);
								}
							});
						}
					});
			},
			// 获取uuid
			getUUID () {
				return new Date().getTime();
			},
			// 返回
			back() {
				this.parent.showFlag = true;
				this.parent.addOrUpdateFlag = false;
				this.parent.ncsecondhandhouseCrossAddOrUpdateFlag = false;
				this.parent.contentStyleChange();
			},
			coverUploadChange(fileUrls) {
				this.ruleForm.cover = fileUrls;
			},
		}
	};
</script>
<style lang="scss" scoped>
	.addEdit-block {
		padding: 30px;
		background: none;
		width: 100%;
	}
	.add-update-preview {
		border-radius: 10px;
		padding: 40px 30px;
		background: #ffffff;
		border-color: #eee;
		border-width: 0px 0 0;
		border-style: solid;
	}
	.amap-wrapper {
		width: 100%;
		height: 500px;
	}
	
	.search-box {
		position: absolute;
	}
	
	.el-date-editor.el-input {
		width: auto;
	}
	.add-update-preview /deep/ .el-form-item {
		border: 0px solid #eee;
		padding: 0;
		margin: 0 0 26px 0;
		display: inline-block;
		width: 49%;
	}
	.add-update-preview .el-form-item /deep/ .el-form-item__label {
		padding: 0 10px 0 0;
		color: #6e6e6e;
		font-weight: 500;
		width: 180px;
		font-size: 15px;
		line-height: 40px;
		text-align: right;
	}
	
	.add-update-preview .el-form-item /deep/ .el-form-item__content {
		margin-left: 180px;
	}
	.add-update-preview .el-form-item span.text {
		padding: 0 10px;
		color: #333;
		background: none;
		font-weight: 500;
		display: inline-block;
		font-size: 15px;
		line-height: 40px;
		min-width: 50%;
	}
	
	.add-update-preview .el-input {
		width: 100%;
	}
	.add-update-preview .el-input /deep/ .el-input__inner {
		border: 1px solid #E8E8E8;
		border-radius: 0px;
		padding: 0 12px;
		color: #666;
		background: #fff;
		width: 100%;
		font-size: 15px;
		min-width: 50%;
		height: 40px;
	}
	.add-update-preview .el-input /deep/ .el-input__inner[readonly="readonly"] {
		border: 0px solid #ccc;
		cursor: not-allowed;
		border-radius: 0px;
		padding: 0 12px;
		color: #666;
		background: none;
		width: auto;
		font-size: 15px;
		height: 40px;
	}
	.add-update-preview .el-input-number {
		text-align: left;
		width: 100%;
	}
	.add-update-preview .el-input-number /deep/ .el-input__inner {
		text-align: left;
		border: 1px solid #E8E8E8;
		border-radius: 0px;
		padding: 0 12px;
		color: #666;
		background: #fff;
		width: 100%;
		font-size: 15px;
		min-width: 50%;
		height: 40px;
	}
	.add-update-preview .el-input-number /deep/ .is-disabled .el-input__inner {
		text-align: left;
		border: 0px solid #ccc;
		cursor: not-allowed;
		border-radius: 0px;
		padding: 0 12px;
		color: #666;
		background: none;
		width: auto;
		font-size: 15px;
		height: 40px;
	}
	.add-update-preview .el-input-number /deep/ .el-input-number__decrease {
		display: none;
	}
	.add-update-preview .el-input-number /deep/ .el-input-number__increase {
		display: none;
	}
	.add-update-preview .el-select {
		width: 100%;
	}
	.add-update-preview .el-select /deep/ .el-input__inner {
		border: 1px solid #E8E8E8;
		border-radius: 0px;
		padding: 0 10px;
		color: #666;
		background: #fff;
		width: 100%;
		font-size: 15px;
		height: 40px;
	}
	.add-update-preview .el-select /deep/ .is-disabled .el-input__inner {
		border: 0;
		cursor: not-allowed;
		border-radius: 4px;
		padding: 0 10px;
		color: #666;
		background: none;
		width: auto;
		font-size: 15px;
		height: 34px;
	}
	.add-update-preview .el-date-editor {
		width: 100%;
	}
	.add-update-preview .el-date-editor /deep/ .el-input__inner {
		border: 1px solid #E8E8E8;
		border-radius: 0px;
		padding: 0 10px 0 30px;
		color: #666;
		background: #fff;
		width: 100%;
		font-size: 15px;
		height: 40px;
	}
	.add-update-preview .el-date-editor /deep/ .el-input__inner[readonly="readonly"] {
		border: 0;
		cursor: not-allowed;
		border-radius: 0px;
		padding: 0 10px 0 30px;
		color: #666;
		background: none;
		width: auto;
		font-size: 15px;
		height: 40px;
	}
	.add-update-preview .viewBtn {
		border: 1px solid #E8E8E8;
		cursor: pointer;
		border-radius: 0px;
		padding: 0 15px;
		margin: 0 20px 0 0;
		color: #666;
		background: #fff;
		width: auto;
		font-size: 15px;
		line-height: 34px;
		height: 34px;
		.iconfont {
			margin: 0 2px;
			color: #666;
			font-size: 16px;
			height: 34px;
		}
	}
	.add-update-preview .viewBtn:hover {
		opacity: 0.8;
	}
	.add-update-preview .downBtn {
		border: 1px solid #E8E8E8;
		cursor: pointer;
		border-radius: 0px;
		padding: 0 15px;
		margin: 0 20px 0 0;
		color: #666;
		background: #fff;
		width: auto;
		font-size: 15px;
		line-height: 34px;
		height: 34px;
		.iconfont {
			margin: 0 2px;
			color: #666;
			font-size: 16px;
			height: 34px;
		}
	}
	.add-update-preview .downBtn:hover {
		opacity: 0.8;
	}
	.add-update-preview .unBtn {
		border: 0;
		cursor: not-allowed;
		border-radius: 4px;
		padding: 0 0px;
		margin: 0 20px 0 0;
		outline: none;
		color: #999;
		background: none;
		width: auto;
		font-size: 15px;
		line-height: 40px;
		height: 40px;
		.iconfont {
			margin: 0 2px;
			color: #fff;
			display: none;
			font-size: 14px;
			height: 34px;
		}
	}
	.add-update-preview .unBtn:hover {
		opacity: 0.8;
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
		border: 1px solid #E8E8E8;
		cursor: pointer;
		border-radius: 0px;
		color: #666;
		background: #fff;
		width: 90px;
		font-size: 24px;
		line-height: 60px;
		text-align: center;
		height: 60px;
	}
	
	.add-update-preview /deep/ .el-upload-list .el-upload-list__item {
		border: 1px solid #E8E8E8;
		cursor: pointer;
		border-radius: 0px;
		color: #666;
		background: #fff;
		width: 90px;
		font-size: 24px;
		line-height: 60px;
		text-align: center;
		height: 60px;
	}
	
	.add-update-preview /deep/ .el-upload .el-icon-plus {
		border: 1px solid #E8E8E8;
		cursor: pointer;
		border-radius: 0px;
		color: #666;
		background: #fff;
		width: 90px;
		font-size: 24px;
		line-height: 60px;
		text-align: center;
		height: 60px;
	}
	.add-update-preview /deep/ .el-upload__tip {
		color: #666;
		font-size: 15px;
	}
	
	.add-update-preview .el-textarea /deep/ .el-textarea__inner {
		border: 1px solid #E8E8E8;
		border-radius: 0px;
		padding: 12px;
		color: #666;
		background: #fff;
		width: 100%;
		font-size: 15px;
		min-height: 150px;
		height: auto;
	}
	.add-update-preview .el-textarea /deep/ .el-textarea__inner[readonly="readonly"] {
				border: 0;
				cursor: not-allowed;
				border-radius: 0px;
				padding: 12px;
				color: #666;
				background: none;
				width: auto;
				font-size: 15px;
				min-width: 400px;
				height: auto;
			}
	.add-update-preview .el-form-item.btn {
		padding: 0;
		margin: 20px 0 0;
		.btn1 {
			border: 0px solid #ccc;
			cursor: pointer;
			border-radius: 6px;
			padding: 0 10px;
			margin: 0 10px 0 0;
			color: #fff;
			background: #0356bb;
			width: auto;
			font-size: 16px;
			min-width: 110px;
			height: 40px;
			.iconfont {
				margin: 0 2px;
				color: #fff;
				display: none;
				font-size: 14px;
				height: 40px;
			}
		}
		.btn1:hover {
			opacity: 0.8;
		}
		.btn2 {
			border: 0px solid #ccc;
			cursor: pointer;
			border-radius: 6px;
			padding: 0 10px;
			margin: 0 10px 0 0;
			color: #fff;
			background: #39c9ee;
			width: auto;
			font-size: 16px;
			min-width: 110px;
			height: 40px;
			.iconfont {
				margin: 0 2px;
				color: #fff;
				display: none;
				font-size: 14px;
				height: 34px;
			}
		}
		.btn2:hover {
			opacity: 0.8;
		}
		.btn3 {
			border: 0px solid #ccc;
			cursor: pointer;
			border-radius: 6px;
			padding: 0 10px;
			margin: 0 10px 0 0;
			color: #fff;
			background: #6ea0dc;
			width: auto;
			font-size: 16px;
			min-width: 110px;
			height: 40px;
			.iconfont {
				margin: 0 2px;
				color: #fff;
				display: none;
				font-size: 14px;
				height: 40px;
			}
		}
		.btn3:hover {
			opacity: 0.8;
		}
		.btn4 {
			border: 0px solid #ccc;
			cursor: pointer;
			border-radius: 6px;
			padding: 0 10px;
			margin: 0 10px 0 0;
			color: #fff;
			background: #4abcff;
			width: auto;
			font-size: 16px;
			min-width: 110px;
			height: 40px;
			.iconfont {
				margin: 0 2px;
				color: #fff;
				display: none;
				font-size: 14px;
				height: 40px;
			}
		}
		.btn4:hover {
			opacity: 0.8;
		}
		.btn5 {
			border: 0px solid #ccc;
			cursor: pointer;
			border-radius: 6px;
			padding: 0 10px;
			margin: 0 10px 0 0;
			color: #fff;
			background: #0977fd;
			width: auto;
			font-size: 16px;
			min-width: 110px;
			height: 40px;
			.iconfont {
				margin: 0 2px;
				color: #fff;
				display: none;
				font-size: 14px;
				height: 40px;
			}
		}
		.btn5:hover {
			opacity: 0.8;
		}
	}
</style>
