<template>
	<div class="forum-preview">
		<div class="forum-title">
			<div>在线交流</div>
		</div>
		<el-form :inline="true" :model="formSearch" class="list-form-pv">
			<el-form-item class="search-item">
				<el-input v-model="title" placeholder="标题"></el-input>
			</el-form-item>
			<div class="search-btn-item">
				<el-button class="searchBtn" type="primary" @click="getForumList(1)">
					<span class="icon iconfont icon-fangdajing07"></span>
					查询
				</el-button>
				<el-button class="pubBtn" type="primary" @click="toForumAdd">
					<span class="icon iconfont icon-tianjia14"></span>
					发布帖子
				</el-button>
			</div>
		</el-form>
		<div class="category-list">
			<div class="item" @click="categoryClick(0)" :class="categoryIndex == 0 ? 'active' : ''">全部</div>
			<div v-for="(item,index) in categoryList" @click="categoryClick(index+1)" :key="index" class="item" :class="categoryIndex == index+1 ? 'active' : ''">{{item.typename}}</div>
		</div>
		<div class="z-box">
			<div class="section-content" v-for="item in forumList" :key="item.id" @click.stop="toForumDetail(item)">
				<img class="item-img" :src="$config.baseUrl + item.cover.split(',')[0]" @click.stop="imgPreView($config.baseUrl + item.cover.split(',')[0])" />
				<div class="item-title">{{item.title}}</div>
				<div class="item-user">发布人：{{item.isanon==1&&item.userid!=userid?'匿名':item.username}}</div>
				<div class="item-time">{{item.addtime}}</div>
			</div>
		</div>
		<el-pagination
			background
			id="pagination" class="pagination"
			:pager-count="7"
			:page-size="pageSize"
			:page-sizes="pageSizes"
			prev-text="上一页"
			next-text="下一页"
			:hide-on-single-page="false"
			:layout='["total","prev","pager","next","sizes","jumper"].join()'
			:total="total"
			@current-change="curChange"
			@prev-click="prevClick"
			@next-click="nextClick"
			></el-pagination>
		<el-dialog title="预览图" :visible.sync="previewVisible" width="50%">
			<img :src="previewImg" alt="" style="width: 100%;">
		</el-dialog>
	</div>
</template>

<script>
	export default {
		//数据集合
		data() {
			return {
				formSearch: {},
				title: '',
				layouts: '',
				forumList: [],
				total: 1,
				pageSize: 10,
				pageSizes: [],
				totalPage: 1,
				previewImg: '',
				previewVisible: false,
				userid: localStorage.getItem('frontUserid'),
				categoryIndex: 0,
				categoryList: [],
			}
		},
		created() {
			this.getCategoryList()
			this.getForumList(1);
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
			categoryClick(index) {
				this.categoryIndex = index
				this.getForumList()
			},
			imgPreView(url){
				this.previewImg = url
				this.previewVisible = true
			},
			getForumList(page) {
				let params = {page, limit: this.pageSize, isdone: '开放', sort: 'istop,toptime', order: 'desc,desc',delflag: 0};
				let searchWhere = {};
				if(this.title != '') searchWhere.title = '%' + this.title + '%';
				if(this.categoryIndex!=0){
					searchWhere.typename = this.categoryList[this.categoryIndex - 1].typename
				}
				this.$http.get('forum/flist', {params: Object.assign(params, searchWhere)}).then(res => {
					if (res.data.code == 0) {
						this.forumList = res.data.data.list;
						this.total = res.data.data.total;
						this.pageSize = Number(res.data.data.pageSize);
						this.totalPage = res.data.data.totalPage;
						if(this.pageSizes.length==0){
							this.pageSizes = [this.pageSize, this.pageSize*2, this.pageSize*3, this.pageSize*5];
						}
					}
				});
			},
			curChange(page) {
				this.getForumList(page);
			},
			prevClick(page) {
				this.getForumList(page);
			},
			nextClick(page) {
				this.getForumList(page);
			},
			toForumAdd() {
				this.$router.push('/index/forumAdd');
			},
			toForumDetail(item) {
				this.$router.push({path: '/index/forumDetail', query: {id: item.id}});
			}
		}
	}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
	.forum-preview {
				padding: 0px;
				margin: 20px auto;
				background: rgb(255, 255, 255);
				width: 1200px;
				position: relative;
				.forum-title {
						background: #f7db61;
						width: 100%;
						border-bottom: 1px solid #1f292f;
						div {
								padding: 0 10px;
								color: #333;
								width: 100%;
								font-size: 24px;
								line-height: 50px;
								text-align: center;
								height: 50px;
							}
		}
		.list-form-pv {
						padding: 0px;
						margin: 20px 0 0;
						background: none;
						display: flex;
						width: 100%;
						align-items: center;
						flex-wrap: wrap;
						height: auto;
						.search-item {
								margin: 0;
								/deep/ .el-form-item__content {
										display: flex;
										align-items: center;
									}
				.el-input {
										width: 100%;
									}
				.el-input /deep/ .el-input__inner {
										border: 1px solid #ddd;
										border-radius: 4px;
										padding: 0 10px;
										margin: 0;
										color: #888;
										width: 280px;
										font-size: 16px;
										line-height: 42px;
										height: 42px;
									}
			}
			.search-btn-item {
								display: flex;
								.searchBtn {
										cursor: pointer;
										border: 0;
										border-radius: 4px;
										padding: 0px 15px;
										margin: 0 10px 0;
										background: #f7db61;
										width: auto;
										font-size: 16px;
										line-height: 42px;
										height: 42px;
										.icon {
												margin: 0 2px 0 0;
												color: #000;
											}
				}
				
				.searchBtn:hover {
										opacity: 0.8;
									}
				
				.pubBtn {
										cursor: pointer;
										border: 1px solid #f7db6180;
										border-radius: 4px;
										padding: 0px 15px;
										margin: 0 10px 0 0;
										color: #000;
										background: #f7db6130;
										width: auto;
										font-size: 16px;
										line-height: 42px;
										height: 42px;
										.icon {
												margin: 0 2px 0 0;
												color: #000;
												font-size: 16px;
											}
				}
				
				.pubBtn:hover {
										opacity: 0.8;
									}
			}
		}
		.category-list {
						padding: 10px;
						margin: 30px 0;
						background: #fff;
						display: flex;
						width: 100%;
						flex-wrap: wrap;
						height: auto;
						.item {
								cursor: pointer;
								border-radius: 4px;
								padding: 0 10px;
								margin: 0 10px 0 0;
								color: #666;
								background: none;
								width: auto;
								font-size: 16px;
								line-height: 36px;
								text-align: center;
								min-width: 80px;
							}
			
			.item:hover {
								color: #333;
								background: #f7db61;
							}
			
			.item.active {
								color: #333;
								background: #f7db61;
							}
		}
		.z-box {
						padding: 0px;
						margin: 20px 0;
						width: 100%;
						.section-content {
								cursor: pointer;
								padding: 0 0 10px;
								margin: 0 0 10px;
								background: #fff;
								display: flex;
								width: 100%;
								border-color: #f7db6180;
								border-width: 0 0 1px;
								align-items: center;
								border-style: solid;
								.item-img {
										border-radius: 0px;
										margin: 0 10px 0 0;
										object-fit: cover;
										width: 100px;
										transition: all .4s;
										height: 80px;
									}
				.item-title {
										overflow: hidden;
										color: #666;
										white-space: nowrap;
										flex: 1;
										font-weight: 600;
										width: auto;
										font-size: 16px;
										line-height: 40px;
										text-overflow: ellipsis;
									}
				.item-user {
										margin: 0 20px 0 0;
										color: #999;
										font-size: 15px;
										line-height: 2;
									}
				.item-time {
										color: #999;
										font-size: 15px;
										line-height: 1.5;
									}
			}
			.section-content:hover {
								.item-title {
										color: #000;
									}
				.item-user {
									}
				.item-time {
									}
			}
		}
	}
</style>
