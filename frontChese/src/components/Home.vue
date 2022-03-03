<template>
  <div class="home">
    <el-col :span="14">
      <el-row>
        <select name="" id="" v-model="selectID" @click="getID()" style="background: bisque; height: 40px; border-radius: 6px; margin-top:10px ">
          <option value="">  --选择回放棋局--  </option>
          <option v-for='item in orgList'>{{item.id}}  {{item.name}}  {{item.time}}</option>
        </select>
        <el-button @click="review_select()" style=" background: bisque; margin: 12px; cursor: pointer">确认回放</el-button>
      </el-row>

      <el-row class="chess" display="margin-top:20px">
        <el-input v-model="inputname" placeholder="请输入玩家姓名" style="display: inline-table; width: 20%;  margin-right:8px"></el-input>
        <el-input v-model="inputsize" placeholder="请输入棋盘大小" style="display: inline-table; width: 20%;  margin-left:8px"></el-input>
        <el-button @click="start()" style=" background: bisque; margin: 12px; cursor: pointer">开始</el-button>
      </el-row>

      <el-row display="margin-bottom: 30px">
        <el-button @click="keep()" style=" background: bisque; margin: 12px; cursor: pointer;">保存本局</el-button>
        <el-button @click='rule()' style=" background: bisque; margin: 12px; cursor: pointer">规则说明</el-button>
        <!--<el-button @click='board()' style=" background: bisque; margin: 12px; cursor: pointer">查看排行榜</el-button>-->
        <el-dialog class="msg" title="游戏规则" :visible.sync="ruleVisible" width="40%" :close-on-click-modal=false>
          <el-span>{{rules}}</el-span>
        </el-dialog>
      </el-row>

      <canvas id="myCanvas" ref="canvas" width="480" height="480">当前浏览器不支持Canvas</canvas>
    </el-col>

    <el-col :span="8" style="margin-top: 20px;">
      <el-span style="font-size: 26px; font-weight: bold;">排行榜</el-span>

      <el-row>
        <el-button @click="board()" style=" background: bisque; margin-top: 20px; cursor: pointer; float:right">更新</el-button>
      </el-row>

      <el-table :data="boardData" :header-cell-style="{'text-align':'center'}">
        <el-table-column property="position" label="排名" align="center" width="100"></el-table-column>
        <el-table-column property="id" label="棋局id" align="center" width="100"></el-table-column>
        <el-table-column property="name" label="姓名" align="center" width="100"></el-table-column>
        <el-table-column property="size" label="棋盘" align="center" width="50"></el-table-column>
        <el-table-column property="left" label="剩余棋子" align="center" width="100"></el-table-column>

      </el-table>
    </el-col>
    <el-divider></el-divider>
    <company ref="company" @board="parentBoard"></company>

    <el-dialog class="msg" title="棋局结束" :visible.sync="flag" width="40%" :close-on-click-modal=false>
      <el-span>本局已无法继续移动棋子，请选择是否保存</el-span>
      <div slot="footer">
        <el-button @click="cancle()" style="float:right; margin-left:8px">取消</el-button>
        <el-button @click="keep()" type="primary" style="float:right; margin-right:8px">保存</el-button>
      </div>
    </el-dialog>

  </div>
</template>

<script>
  import company from "./company";
  import qs from 'qs';
 

  export default {
    name: 'chess',
    components: {
      company,
    },
    data() {
      return {
        boardData: [],
        rules: "",
        ruleVisible:false,
        inputsize:'',
        inputname:'',
        size: '11',
        mid: 0,
        pieceMapArr: [], //记录棋盘落子情况
        pieceColor: ["black", "red"],//棋子颜色
        step: 0, //记录当前步数，而且size相同的时候，step越大说明剩余棋子越少
        x1: -1,
        y1: -1,
        x2: -1,
        y2: -1,
        flag: false,
        canMove: false,
        orgList:[],
        endness: '',
        history:[],
        toggle: true //true为canvas,false为dom
      }
    },
    mounted() {
      const myCanvas = document.getElementById("myCanvas");
      if (!myCanvas.getContext) {
        alert("当前浏览器不支持Canvas.");
        this.toggle = false;
        return;
      } else {
        console.log("当前浏览器支持Canvas", this.toggle)
        this.board();
        this.initPieceArr();
        this.repaint();
        this.drawpieceBoard(this.pieceMapArr);
        const canvas = this.$refs.canvas;
        // 添加点击监听事件
        canvas.addEventListener("click", e => {
          if (this.flag) {
            alert("游戏结束,请重新开始~");
            return;
          }
          //判断点击范围是否越出棋盘
          if (e.offsetX < 25 || e.offsetX > 450 || e.offsetY < 25 || e.offsetY > 450) {
            return;
          }
          let dx = Math.floor((e.offsetX + 15) / 30) * 30;
          let dy = Math.floor((e.offsetY + 15) / 30) * 30;

          let x = dx / 30;
          let y = dy / 30;

          if (this.x1 == -1) {  //点击的第一个棋子

            this.x1 = x;
            this.y1 = y;
            this.drawPiece(x, y, this.pieceColor[1]); //点击棋子变红
            console.log("点击第一个位置：", this.x1, this.y1)

          } else {

            this.x2 = x;
            this.y2 = y;
            console.log("点击第二个位置：", this.x2, this.y2)

            if (this.x1 == this.x2 && this.y1 == this.y2) {

              this.drawPiece(this.x1, this.y1, this.pieceColor[0]);
              this.x1 = -1;
              this.y1 = -1;
            }
            else {

              this.move();
              if (this.canMove == true) {   //可以移动棋子
                this.step++;
                this.x1 = -1;
                this.y1 = -1;
                this.checkEnd();
              }
            }
          }
        });
      }
    },

    methods: {
      //查看排行榜
      board() {
        this.$http.get('http://127.0.0.1:8000/api/board')
          .then((response) => {
            var res = JSON.parse(response.bodyText);
            if (res.error_num == 0) {
              console.log("board res: ", res.board)
              this.boardData = res.board;
            }
          })
      },
      dialogboard: function () {
         this.$refs.company.showBoard()
      },
      parentBoard(obj) {
        console.log("parent: ", obj)
      },
      //查看规则
      rule: function () {
        this.rules = "1、输入玩家姓名，并设置棋盘大小，点击“开始”\n\n2、每次下棋时：第一次点击想要移动的黑棋，第二次点击目标空位\n\n3、点击“保存本局”可成功保存当前棋局，便于回放查看\n\n4、当棋盘大小相同时，剩余棋子少数者为胜"

        //this.rules = this.rules.replace(/\n/g, <el-br>)
        this.ruleVisible = true;
      },
      parentRule(obj) {
        console.log("parent: ", obj)
      },

      //获取所有玩家信息
      getID: function () {
        this.$http.get('http://127.0.0.1:8000/api/getid')
          .then((response) => {
            var res = JSON.parse(response.bodyText);

            if (res.error_num == 0) {
              console.log("getid结果：", res.allList)
              this.orgList = res.allList;
            } else {
              alert("error!")
            }
          })
      },

      //棋局开始
      start() {
        this.playerName = this.inputname;
        this.size = this.inputsize;

        this.repaint();
        this.initPieceArr();
        this.drawpieceBoard(this.pieceMapArr);
        this.step = 0;
        this.flag = false;
        this.history = [];

      },


      //选局回放
      review_select() {
        let i = 0;

        //参数selectID是点击选定的棋局条目
        this.$http.get('http://127.0.0.1:8000/api/review', { params: { id: this.selectID } })
          .then((response) => {
            var res = JSON.parse(response.bodyText);
            if (res.error_num == 0) {

              this.size = res.size
              this.repaint();
              this.initPieceArr();
              this.drawpieceBoard(this.pieceMapArr);

              let r = qs.parse(res.list)
              console.log("rs: ",r)

              let i = 0
              let timer = setInterval(() => {
                let x1 = r[i]['x1']
                let y1 = r[i]['y1']
                let x2 = r[i]['x2']
                let y2 = r[i]['y2']
                let x3 = r[i]['x3']
                let y3 = r[i]['y3']

                this.pieceMapArr[x1][y1] = 0;
                this.pieceMapArr[x2][y2] = 0;
                this.pieceMapArr[x3][y3] = 1;

                let tmp = 0;

                let tmr = setInterval(() => {
                  if (tmp == 0) {
                    this.drawPiece(x2, y2, this.pieceColor[1]);
                    this.drawPiece(x1, y1, this.pieceColor[1]);
                    tmp = 1;
                  } else {
                    this.drawPiece(x3, y3, this.pieceColor[0]);
                    this.drawPiece(x2, y2, 'bisque');
                    this.drawPiece(x1, y1, 'bisque');
                    clearInterval(tmr);
                  }
                }, 500)
                if (i < res.stepCnt) {
                  i++;
                } else {
                  clearInterval(timer);
                }
              },1000)

            }else{
              console.log("error!",res.msg)
            }
          })
      },

      //下一次棋
      move() {
        let x = Math.floor((this.x1 + this.x2) / 2);
        let y = Math.floor((this.y1 + this.y2) / 2);
        if (this.pieceMapArr[this.x2][this.y2] == 0 && this.pieceMapArr[this.x1][this.y1] == 1 && this.pieceMapArr[x][y] == 1) {
          this.history.push({  //加入历史记录
            'x1': this.x1, 'y1': this.y1, 'x2': x,
            'y2': y, 'x3': this.x2, 'y3': this.y2
          })

          this.pieceMapArr[this.x1][this.y1] = 0;
          this.pieceMapArr[x][y] = 0;
          this.pieceMapArr[this.x2][this.y2] = 1;

          this.drawPiece(this.x2, this.y2, this.pieceColor[0]);
          this.drawPiece(x, y, 'bisque');
          this.drawPiece(this.x1, this.y1, 'bisque');

          this.canMove = true;
        }
        else
          this.canMove = false;
      },

      //判断是否结束
      checkEnd() {
        let end = true;
        for (let x = 1; x <= this.size; ++x) {
          for (let y = 1; y <= this.size; ++y) {
            if (this.pieceMapArr[x][y] == 1) {
              if (y + 2 <= this.size && this.pieceMapArr[x][y + 1] == 1 && this.pieceMapArr[x][y + 2] == 0)
                end = false;
              if (y - 2 >= 1 && this.pieceMapArr[x][y - 1] == 1 && this.pieceMapArr[x][y - 2] == 0)
                end = false;
              if (x + 2 <= this.size && this.pieceMapArr[x + 1][y] == 1 && this.pieceMapArr[x + 2][y] == 0)
                end = false;
              if (x - 2 >= 1 && this.pieceMapArr[x - 1][y] == 1 && this.pieceMapArr[x - 2][y] == 0)
                end = false;
            }
          }
        }
        if (end == true) {
          this.endness = "本局已无法继续移动棋子";
          this.step--;
          this.flag = true;
        }
      },

      //保存本局
      keep() {
        let list = qs.stringify(this.history)
        this.$http.get('http://127.0.0.1:8000/api/keeptest', { params: { name: this.playerName, size: this.size, stepCnt: this.step, list: list } })
          .then((response) => {
            var res = JSON.parse(response.bodyText)
            if (res.error_num == 0) {
              alert("已成功保存");
              let r = qs.parse(response.bodyText)   //可以解析出数组
              console.log("r:  ",r)
            } else {
              console.log("保存失败：", res.msg);
            }
          })
      },

      //不保存
      cancle() {
        this.flag = false
      },

      //初始化棋盘数组
      initPieceArr() {
        this.pieceMapArr = [];
        for (let i = 0; i <= this.size; i++) {
          this.pieceMapArr[i] = [];
          for (let j = 0; j <= this.size; j++) {
            this.pieceMapArr[i][j] = 1;
          }
        }
        this.mid = Math.floor(this.size / 2 + 1);
        console.log("this.mid: ", this.mid)
        this.pieceMapArr[this.mid][this.mid] = 0;
      },


      // 绘制棋盘
      drawpieceBoard(arr) {
        //初始化棋盘数组
        //this.pieceArr();
        //canvas 绘制
        let canvas = this.$refs.canvas
        // 调用canvas元素的getContext 方法访问获取2d渲染的上下文
        let context = canvas.getContext("2d");
        context.strokeStyle = '#666'

        for (let i = 0; i <= this.size; i++) {
          //落在方格(canvas 的宽高是450)
          context.moveTo(15 + i * 30, 15)
          context.lineTo(15 + i * 30, 15 * (this.size * 2 + 1))
          context.stroke()
          context.moveTo(15, 15 + i * 30)
          context.lineTo(15 * (this.size * 2 + 1), 15 + i * 30)
          context.stroke()
        }

        for (let i = 1; i <= this.size; i++) {
          for (let j = 1; j <= this.size; j++) {
            if (arr[i][j] != 0) {  //非0的数组位置棋子全都画成黑色
              this.drawPiece(i, j, this.pieceColor[0]);
            }
          }
        }
      },

      //绘制棋子
      drawPiece(x, y, color) {
        let dx = x * 30;
        let dy = y * 30
        let canvas = this.$refs.canvas
        let context = canvas.getContext("2d");
        context.beginPath(); //开始一条路径或重置当前的路径
        context.arc(dx, dy, 13, 0, Math.PI * 2, false);
        context.closePath();
        context.fillStyle = color;
        context.fill();
      },

      //重画
      repaint() {
        let canvas = this.$refs.canvas;
        let context = canvas.getContext("2d");
        canvas.width = this.size * 30 + 30;
        canvas.height = this.size * 30 + 30;
        //context.clearRect(0, 0, canvas.width, this.size * 30 + 30t);
        context.fillStyle = "bisque";
        //console.log("长宽：", canvas.width, canvas.height)
        context.fillRect(0, 0, canvas.width, canvas.height);
        context.beginPath();
        context.closePath();
      },


       //棋局回放
       review() {
        this.repaint();
        this.initPieceArr();
        this.drawpieceBoard(this.pieceMapArr);

        let count=0

        this.timer = setInterval(() => {
          this.$http.get('http://127.0.0.1:8000/api/sendpos', { params: { count: count} })
            .then((response) => {

              var res = JSON.parse(response.bodyText)

              this.pieceMapArr[res.x1][res.y1] = 0;
              this.pieceMapArr[res.x2][res.y2] = 0;
              this.pieceMapArr[res.x3][res.y3] = 1;

              let tmp = 0;

              let tmr = setInterval(() => {
                if (tmp == 0) {
                  this.drawPiece(res.x2, res.y2, this.pieceColor[1]);
                  this.drawPiece(res.x1, res.y1, this.pieceColor[1]);
                  tmp = 1;
                } else {
                  this.drawPiece(res.x3, res.y3, this.pieceColor[0]);
                  this.drawPiece(res.x2, res.y2, 'bisque');
                  this.drawPiece(res.x1, res.y1, 'bisque');
                  clearInterval(tmr);
                }
              },500)
              //this.drawPiece(res.x3, res.y3, this.pieceColor[0]);
              //this.drawPiece(res.x2, res.y2, 'bisque');
              //this.drawPiece(res.x1, res.y1, 'bisque');

              if (res.end == 0) {
                count++;
              }
              else {
                clearInterval(this.timer);
                return;
              }
            })
        }, 1000)
      },

    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  body {
    margin: 0;
    padding: 0;
  }

  #app {
    padding-left: 30%;
    width: 500px;
  }

  .h2Title {
    text-align: center;
  }

  #app h3 {
    color: red;
  }

  .Fbuttons {
    margin-bottom: 1rem;
  }

  .main {
    background-color: bisque;
    width: 30rem;
  }

  .restart, .regret, .makesize {
    background: bisque;
    padding: 6px 10px;
    border-radius: 6px;
    font-size: 12px;
    cursor: pointer;
  }

  #chess {
    position: relative;
    width: 440px;
    height: 450px;
    padding-left: 30px;
    padding-top: 30px;
    background-color: bisque;
  }

    #chess .squre {
      width: 28px;
      height: 28px;
      border: 1px solid #666;
      float: left;
    }

  #box01 .squre:hover {
    background-color: pink;
  }

  #box01 {
    position: absolute;
    margin: 0 auto;
    width: 450px;
    height: 450px;
    top: 15px;
    left: 15px;
  }

    #box01 .qz {
      /* width: 28px;
        height: 28px; */
      width: 30px;
      height: 30px;
      border: 0px solid #C7C7C7;
      float: left;
      border-radius: 50%;
      /* margin: 1px; */
    }

      #box01 .qz:hover {
        background-color: pink;
      }

  .toggle {
    float: right;
  }

  .size {
    float: center;
  }
  .msg {
    font-size: 30px;
    white-space: pre-wrap; /*这是重点。文本换行*/
    margin: 20px auto;
    text-align: left;
  }
  .lightgreen-box {
    background-color: bisque;
    height: 500px;
  }
</style>
