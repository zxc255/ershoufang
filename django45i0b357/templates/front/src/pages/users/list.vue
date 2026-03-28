<template>
	<div>
		<div class="breadcrumb-preview">
			<el-breadcrumb :separator="'>'">
				<el-breadcrumb-item class="item1" to="/"><a>首页</a></el-breadcrumb-item>
				<el-breadcrumb-item class="item2" v-for="(item, index) in breadcrumbItem" :key="index"><a>{{item.name}}</a></el-breadcrumb-item>
			</el-breadcrumb>
		</div>
		<div v-if="centerType" class="back_box">
			<el-button class="backBtn" size="mini" @click="backClick">
				<span class="icon iconfont icon-jiantou33"></span>
				<span>返回</span>
			</el-button>
		</div>
		<div class="list-preview">
			<el-form :inline="true" :model="formSearch" class="list-form-pv">
				<el-form-item class="list-item">
					<div class="lable">用户名：</div>
					<el-input v-model="formSearch.username" placeholder="用户名" @keydown.enter.native="getList(1, curFenlei)" clearable></el-input>
				</el-form-item>
				<el-button class="list-search-btn" v-if=" true " type="primary" @click="getList(1, curFenlei)">
					<i class="el-icon-search"></i>
					查询
				</el-button>
				<el-button class="list-add-btn" v-if="btnAuth('users','新增')" type="primary" @click="add('/index/usersAdd')">
					<i class="el-icon-circle-plus-outline"></i>
					添加
				</el-button>
			</el-form>
			<div class="select2">
				<div class="select2-list" v-for="(item,index) in selectOptionsList" :key="item">
					<div class="label">{{item.name}}：</div>
					<div class="item-body">
						<div class="item" @click="selectClick2(item,-1)" :class="item.check ==-1 ? 'active' : ''">全部</div>
						<div class="item" @click="selectClick2(item,index1)" :class="item.check == index1 ? 'active' : ''" v-for="item1,index1 in item.list" :key="item1">{{item1}}</div>
					</div>
				</div>
			</div>
			<div class="sort_view">
				<el-button class="click-sort-btn" @click="sortClick('clicknum')">
					<span class="icon iconfont icon-liulan04" v-if="sortType!='clicknum'"></span>
					<span class="icon iconfont icon-jiantou23" v-else-if="sortType=='clicknum'&&sortOrder=='desc'"></span>
					<span class="icon iconfont icon-jiantou24" v-else-if="sortType=='clicknum'&&sortOrder=='asc'"></span>
					<span class="text">点击量：</span>
				</el-button>
			</div>
			<div class="list">
				<div class="list6">
					<div v-for="(item,index) in dataList" :key="index" :class="'list-item' + ((index%2) + 1)" @click.stop="toDetail(item)">
						<div class="imgbox">
						</div>
						<div class="infoBox">
							<div class="centerInfo">
							</div>
							<div class="bottomInfo">
								<div class="time_item">
									<span class="icon iconfont" :class="index%2==0?'':''"></span>
									<span class="label">{{index%2==0?'发布时间：':'发布时间：'}}</span>
									<span class="text">{{index%2==0? item.addtime.split(' ')[0]: item.addtime.split(' ')[0]}}</span>
								</div>
								<div class="more_btn" @click.stop="toDetail(item)">
									<span class="text">{{index%2==0?'详情':'详情'}}</span>
									<span class="icon iconfont" :class="index%2==0?'icon-jiantou25':'icon-jiantou25'"></span>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>

	
			<el-pagination
				background
				id="pagination"
				class="pagination"
				:pager-count="7"
				:page-size="pageSize"
				prev-text="上一页"
				next-text="下一页"
				:hide-on-single-page="false"
				:layout='["total","prev","pager","next","sizes","jumper"].join()'
				:total="total"
				:page-sizes="pageSizes"
				@current-change="curChange"
				@size-change="sizeChange"
				@prev-click="prevClick"
				@next-click="nextClick"
				></el-pagination>
			<div class="idea1"></div>
		</div>
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
				selectIndex2: 0,
				selectOptionsList: [],
				layouts: '',
				swiperIndex: -1,
				baseUrl: '',
				breadcrumbItem: [
					{
						name: '管理员'
					}
				],
				formSearch: {
					username: '',
				},
				fenlei: [],
				feileiColumn: '',
				dataList: [],
				total: 1,
				pageSize: 10,
				pageSizes: [],
				totalPage: 1,
				curFenlei: '全部',
				isPlain: false,
				indexQueryCondition: '',
				timeRange: [],
				centerType:false,
				previewImg: '',
				previewVisible: false,
				sortType: 'id',
				sortOrder: 'desc',
			}
		},
		async created() {
			if(this.$route.query.centerType){
				this.centerType = true
			}
			this.baseUrl = this.$config.baseUrl;
			await this.getFenlei();
			let fenlei = '全部'
			if(this.$route.query.homeFenlei){
				fenlei = this.$route.query.homeFenlei
			}
			this.getList(1, fenlei);
		},
		watch:{
			$route(newValue){
				this.getList(1, newValue.query.homeFenlei);
			}
		},
		//方法集合
		methods: {
			selectClick2(row,index) {
				row.check = index
				if(index == -1){
					this.formSearch[row.tableName] = ''
				}else {
					this.formSearch[row.tableName] = row.list[index]
				}
				this.getList()
			},
			add(path) {
				let query = {}
				if(this.centerType){
					query.centerType = 1
				}
				this.$router.push({path: path,query:query});
			},
			async getFenlei() {
			},
			getList(page, fenlei, ref = '') {
				let params = {
					page,
					limit: this.pageSize,
				};
				let searchWhere = {};
				if (this.formSearch.username != '') searchWhere.username = '%' + this.formSearch.username + '%';
				let user = JSON.parse(localStorage.getItem('sessionForm'))
				if (this.sortType) searchWhere.sort = this.sortType
				if (this.sortOrder) searchWhere.order = this.sortOrder
				this.$http.get(`users/${this.centerType?'page':'list'}`, {params: Object.assign(params, searchWhere)}).then(res => {
					if (res.data.code == 0) {
						this.dataList = res.data.data.list;
						this.total = Number(res.data.data.total);
						this.pageSize = Number(res.data.data.pageSize);
						this.totalPage = res.data.data.totalPage;
						if(this.pageSizes.length==0){
							this.pageSizes = [this.pageSize, this.pageSize*2, this.pageSize*3, this.pageSize*5];
						}
					}
				});
			},
			sortClick(type){
				if(this.sortType==type){
					if(this.sortOrder == 'desc'){
						this.sortOrder = 'asc'
					}else{
						this.sortOrder = 'desc'
					}
				}else{
					this.sortType = type
					this.sortOrder = 'desc'
				}
				this.getList(1, '全部')
			},
			curChange(page) {
				this.getList(page);
			},
			prevClick(page) {
				this.getList(page);
			},
			sizeChange(size){
				this.pageSize = size
				this.getList(1);
			},
			nextClick(page) {
				this.getList(page);
			},
			imgPreView(url){
				this.previewImg = url
				this.previewVisible = true
			},
			toDetail(item) {
				let params = {
					id: item.id
				}
				if(this.centerType){
					params.centerType = 1
				}
				this.$router.push({path: '/index/usersDetail', query: params});
			},
			btnAuth(tableName,key){
				if(this.centerType){
					return this.isBackAuth(tableName,key)
				}else{
					return this.isAuth(tableName,key)
				}
			},
			backClick() {
				this.$router.push({path: '/index/center'});
			},
		}
	}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
	.list-preview {
		margin: 0px auto;
		flex-direction: column;
		color: #333;
		background: none;
		display: flex;
		width: 1200px;
		font-size: 16px;
		justify-content: flex-start;
		align-items: flex-start;
		position: relative;
		flex-wrap: wrap;
		.list-form-pv {
			padding: 0;
			margin: 20px 0;
			color: inherit;
			background: none;
			display: flex;
			width: 100%;
			font-size: inherit;
			flex-wrap: wrap;
			height: auto;
			.list-item {
				padding: 0;
				margin: 0 0px 10px 0;
				display: flex;
				font-size: inherit;
				align-items: center;
				flex-wrap: wrap;
				/deep/.el-form-item__content {
					display: flex;
				}
				.lable {
					padding: 0 10px;
					color: #333;
					white-space: nowrap;
					display: inline-block;
					width: auto;
					font-size: 16px;
					line-height: 40px;
				}
				.el-input {
					width: auto;
				}
				.datetimerange {
					border: 1px solid #ccc;
					border-radius: 8px;
					padding: 3px 3px;
					background: #fff;
					width: auto;
					justify-content: center;
				}
				.el-input /deep/ .el-input__inner {
					border: 1px solid #ccc;
					border-radius: 4px;
					padding: 0 10px;
					margin: 0 5px 0 0;
					color: #333;
					width: auto;
					font-size: 16px;
					line-height: 40px;
					height: 40px;
				}
				.el-select {
				}
				.el-select /deep/ .el-input__inner {
				}
				.el-date-editor {
					width: auto;
				}
				.el-date-editor /deep/ .el-input__inner {
					border: 1px solid #ccc;
					border-radius: 4px;
					padding: 0 0px 0 30px;
					margin: 0;
					color: #333;
					width: auto;
					font-size: 16px;
					line-height: 40px;
					height: 40px;
				}
			}
			.list-search-btn {
				cursor: pointer;
				border: 0;
				border-radius: 4px;
				padding: 0px 15px;
				margin: 0 10px 0 10px;
				color: #000;
				background: #f7db6190;
				width: auto;
				font-size: inherit;
				line-height: 40px;
				height: 40px;
				i {
					margin: 0 10px 0 0;
					color: #000;
					font-size: inherit;
				}
			}
			.list-add-btn {
				cursor: pointer;
				border: 0;
				border-radius: 4px;
				padding: 0px 15px;
				margin: 0 10px 0 0;
				color: #000;
				background: #f7db6190;
				width: auto;
				font-size: inherit;
				line-height: 40px;
				height: 40px;
				i {
					margin: 0 10px 0 0;
					color: #000;
					font-size: inherit;
				}
			}
		}
		.select2 {
			padding: 0;
			margin: 20px auto;
			background: none;
			width: 100%;
			font-size: 15px;
			height: auto;
			.select2-list {
				padding: 5px 5px;
				margin: 0 0 10px;
				background: #f7db6130;
				width: 100%;
				height: auto;
				.label {
					padding: 0 5px;
					color: #333;
					font-weight: 500;
					display: inline-block;
					font-size: inherit;
					line-height: 32px;
				}
				.item-body {
					display: inline-block;
					width: auto;
					flex-wrap: wrap;
					height: auto;
					.item {
						border-radius: 4px;
						padding: 0 5px;
						color: inherit;
						background: none;
						display: inline-block;
						font-size: inherit;
						line-height: 32px;
					}
					.item:hover {
						cursor: pointer;
						color: #000;
						background: #f7db61;
					}
					.item.active {
						cursor: pointer;
						color: #000;
						background: #f7db61;
						display: inline-block;
					}
				}
			}
		}
		.sort_view {
			padding: 5px 20px;
			margin: 0px auto;
			color: inherit;
			background: linear-gradient(180deg, rgba(255,244,198,1) 0%, rgba(247,219,97,1) 100%);
			width: 100%;
			font-size: inherit;
			.click-sort-btn {
				border: 0;
				border-radius: 8px;
				padding: 0 5px;
				margin: 0 5px;
				color: inherit;
				background: none;
				font-size: inherit;
				.icon {
					margin: 0 2px 0 0;
					color: inherit;
					font-size: inherit;
					line-height: 40px;
				}
				.text {
					color: inherit;
					font-size: inherit;
					line-height: 40px;
				}
			}
		}
		.list {
			margin: 20px auto;
			background: #fff;
			width: 100%;
			font-size: 15px;
			.index-pv1 .animation-box {
				transform: rotate(0deg) scale(1) skew(0deg, 0deg) translate3d(0px, 0px, 0px);
				z-index: initial;
			}
				
			.index-pv1 .animation-box:hover {
				transform: rotate(0) scale(1.2) skew(0deg, 0deg) translate3d(0px, 0px, 0px);
				-webkit-perspective: 1000px;
				perspective: 1000px;
				transition: 0.3s;
				z-index: 1;
			}
				
			.index-pv1 .animation-box img {
				transform: rotate(0deg) scale(1) skew(0deg, 0deg) translate3d(0px, 0px, 0px);
			}
			
			.index-pv1 .animation-box img:hover {
				transform: rotate(0) scale(0.8) skew(0deg, 0deg) translate3d(0px, 0px, 0px);
				-webkit-perspective: 1000px;
				perspective: 1000px;
				transition: 0.3s;
			}
			.list6 {
				margin: 20px auto 0;
				overflow: hidden;
				width: 100%;
				clear: both;
				.list-item1 {
					margin: 0 0 20px;
					width: 100%;
					border-color: #ddd;
					border-width: 1px;
					border-style: solid;
					height: 300px;
					.imgbox {
						overflow: hidden;
						width: 50%;
						float: left;
						height: 100%;
						.image {
							object-fit: cover;
							width: 100%;
							transition: all 0.6s;
							height: 100%;
						}
					}
					.infoBox {
						padding: 20px 20px 20px 20px;
						align-content: center;
						display: flex;
						width: 50%;
						align-items: center;
						position: relative;
						float: right;
						flex-wrap: wrap;
						height: 100%;
						.name {
							border: 0px solid #eee;
							padding: 0;
							overflow: hidden;
							color: #333;
							white-space: nowrap;
							background: #fff;
							font-weight: normal;
							width: 100%;
							font-size: 18px;
							line-height: 30px;
							text-overflow: ellipsis;
						}
						.price {
							margin: 30px 0 0;
							color: #f00;
							width: 100%;
							font-size: 16px;
							line-height: 1.8;
							.price_text {
								font-size: 22px;
							}
						}
						.centerInfo {
							padding: 10px 0;
							margin: 0px 0 0;
							color: #999;
							display: flex;
							width: 100%;
							font-size: 16px;
							flex-wrap: wrap;
							.publisher_item {
								padding: 0;
								margin: 0 10px 0 0;
								.icon {
									margin: 0 2px 0 0;
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
								.label {
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
								.text {
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
							}
							.like_item {
								padding: 0;
								margin: 0 10px 0 0;
								.icon {
									margin: 0 2px 0 0;
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
								.label {
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
								.text {
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
							}
							.collect_item {
								padding: 0;
								margin: 0 10px 0 0;
								.icon {
									margin: 0 2px 0 0;
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
								.label {
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
								.text {
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
							}
							.view_item {
								padding: 0;
								.icon {
									margin: 0 2px 0 0;
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
								.label {
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
								.text {
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
							}
						}
						.bottomInfo {
							margin: 0px 0 0;
							display: flex;
							width: 100%;
							justify-content: flex-end;
							align-items: center;
							flex-wrap: wrap;
							.time_item {
								padding: 0;
								width: 100%;
								.icon {
									margin: 0 2px 0 0;
									line-height: 1.5;
								}
								.label {
									color: #999;
									font-size: 16px;
									line-height: 1.5;
								}
								.text {
									color: #999;
									font-size: 16px;
									line-height: 1.5;
								}
							}
							.more_btn {
								border: 1px solid #fff;
								border-radius: 20px;
								padding: 10px;
								background: none;
								display: block;
								width: 150px;
								text-align: center;
								.text {
									color: #666;
								}
								.icon {
									color: #666;
								}
							}
						}
					}
				}
				.list-item1:hover {
					cursor: pointer;
					background: #f7db61;
					.imgbox {
						.image {
							transform: scale(1.05);
						}
					}
					.infoBox {
						.name {
							border: 0px solid #ffffff50;
							color: #000;
							background: none;
						}
						.price {
							color: #f00;
							.price_text {
							}
						}
						.centerInfo {
							.publisher_item {
								.icon {
									color: #333;
								}
								.label {
									color: #333;
								}
								.text {
									color: #333;
								}
							}
							.like_item {
								.icon {
									color: #333;
								}
								.label {
									color: #333;
								}
								.text {
									color: #333;
								}
							}
							.collect_item {
								.icon {
									color: #333;
								}
								.label {
									color: #333;
								}
								.text {
									color: #333;
								}
							}
							.view_item {
								.icon {
									color: #333;
								}
								.label {
									color: #333;
								}
								.text {
									color: #333;
								}
							}
						}
						.bottomInfo {
							.time_item {
								.icon {
									color: #333;
								}
								.label {
									color: #333;
								}
								.text {
									color: #333;
								}
							}
							.more_btn {
								background: #ffffff30;
								.text {
									color: #333;
								}
								.icon {
									color: #333;
								}
							}
						}
					}
				}
				.list-item2 {
					margin: 0 0 20px;
					width: 100%;
					border-color: #ddd;
					border-width: 1px;
					border-style: solid;
					height: 300px;
					.imgbox {
						overflow: hidden;
						width: 50%;
						float: right;
						height: 100%;
						.image {
							object-fit: cover;
							width: 100%;
							transition: all 0.6s;
							height: 100%;
						}
					}
					.infoBox {
						padding: 20px 20px 20px 20px;
						align-content: center;
						display: flex;
						width: 50%;
						align-items: center;
						position: relative;
						float: right;
						flex-wrap: wrap;
						height: 100%;
						.name {
							border: 0px solid #eee;
							padding: 0;
							overflow: hidden;
							color: #333;
							white-space: nowrap;
							background: #fff;
							font-weight: normal;
							width: 100%;
							font-size: 18px;
							line-height: 30px;
							text-overflow: ellipsis;
						}
						.price {
							margin: 30px 0 0;
							color: #f00;
							width: 100%;
							font-size: 16px;
							line-height: 1.8;
							.price_text {
								font-size: 22px;
							}
						}
						.centerInfo {
							padding: 10px 0;
							margin: 0px 0 0;
							color: #999;
							display: flex;
							width: 100%;
							font-size: 16px;
							flex-wrap: wrap;
							.publisher_item {
								padding: 0;
								margin: 0 10px 0 0;
								.icon {
									margin: 0 2px 0 0;
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
								.label {
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
								.text {
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
							}
							.like_item {
								padding: 0;
								margin: 0 10px 0 0;
								.icon {
									margin: 0 2px 0 0;
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
								.label {
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
								.text {
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
							}
							.collect_item {
								padding: 0;
								margin: 0 10px 0 0;
								.icon {
									margin: 0 2px 0 0;
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
								.label {
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
								.text {
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
							}
							.view_item {
								padding: 0;
								.icon {
									margin: 0 2px 0 0;
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
								.label {
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
								.text {
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
							}
						}
						.bottomInfo {
							margin: 0px 0 0;
							display: flex;
							width: 100%;
							justify-content: flex-end;
							align-items: center;
							flex-wrap: wrap;
							.time_item {
								padding: 0;
								color: #999;
								width: 100%;
								font-size: 16px;
								.icon {
									margin: 0 2px 0 0;
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
								.label {
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
								.text {
									color: inherit;
									font-size: inherit;
									line-height: 1.5;
								}
							}
							.more_btn {
								border: 1px solid #fff;
								border-radius: 20px;
								padding: 10px;
								display: block;
								width: 150px;
								text-align: center;
								.text {
									color: inherit;
									font-size: inherit;
								}
								.icon {
									color: inherit;
									font-size: inherit;
								}
							}
						}
					}
				}
				.list-item2:hover {
					cursor: pointer;
					background: #f7db61;
					.imgbox {
						.image {
							transform: scale(1.05);
						}
					}
					.infoBox {
						.name {
							border: 0px solid #ffffff50;
							color: #000;
							background: none;
						}
						.price {
							color: #f00;
							.price_text {
							}
						}
						.centerInfo {
							.publisher_item {
								.icon {
									color: #333;
								}
								.label {
									color: #333;
								}
								.text {
									color: #333;
								}
							}
							.like_item {
								.icon {
									color: #333;
								}
								.label {
									color: #333;
								}
								.text {
									color: #333;
								}
							}
							.collect_item {
								.icon {
									color: #333;
								}
								.label {
									color: #333;
								}
								.text {
									color: #333;
								}
							}
							.view_item {
								.icon {
									color: #333;
								}
								.label {
									color: #333;
								}
								.text {
									color: #333;
								}
							}
						}
						.bottomInfo {
							.time_item {
								.icon {
									color: #333;
								}
								.label {
									color: #333;
								}
								.text {
									color: #333;
								}
							}
							.more_btn {
								background: #ffffff30;
								.text {
									color: #333;
								}
								.icon {
									color: #333;
								}
							}
						}
					}
				}
			}
		}
		.idea1 {
			background: none;
			width: 100%;
			order: 90;
			height: 1px;
		}
	}
</style>
