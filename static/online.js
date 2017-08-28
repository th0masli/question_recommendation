var canvas;
var context;
var strokeViewListener;

/**
 * called on window load.
 */
$(document).ready(init);

/**
 * init.
 */
function init(){
		canvas = $('#cv')[0];
    context = canvas.getContext('2d');
		context.imageSmoothingEnabled = true;
    context.strokeStyle = "#0000ff"
		//canvas.style.width = '100%';
		//canvas.style.height = '100%';
    //canvas.width  = canvas.offsetWidth;
    //canvas.height = canvas.offsetHeight;

		canvas.addEventListener('mousedown', ev_canvas, false);
    canvas.addEventListener('mousemove', ev_canvas, false);
    canvas.addEventListener('mouseup',   ev_canvas, false)
		canvas.addEventListener('mouseout',   ev_canvas, false);;
		canvas.addEventListener('touchstart', ev_canvas, false);
		canvas.addEventListener('touchmove', ev_canvas, false);
		canvas.addEventListener('touchend', ev_canvas, false);
		canvas.addEventListener('touchcancel', ev_canvas, false);
  	strokeViewListener = new StrokeViewListener();
}

//init canvas context
function init_canvas(){
    if(strokeViewListener){
        strokeViewListener.started = false;
        strokeViewListener.strokesHistory = {strokes: []};
        strokeViewListener.currentStroke = {points: []};
        strokeViewListener.idx = 0;
    }
	context.clearRect(0, 0, canvas.width, canvas.height);
}

//clear canvas
function ev_clear(ev){
    init_canvas();
}

//strokeview listener
function StrokeViewListener(){
    var strokeViewListener = this;
    this.started = false;
	this.strokesHistory = {strokes: []};
	this.currentStroke = {points: []};
	this.idx = 0;

    this.mousedown = function (ev){
		//data
        strokeViewListener.currentStroke = { points: [] };
        strokeViewListener.idx = 0;
        //UI
        ev.preventDefault();
        context.beginPath();
        context.moveTo(ev._x,ev._y);
        strokeViewListener.started = true;
    };
    this.mousemove = function (ev){
        if(strokeViewListener.started){
            if(strokeViewListener.idx % 1 == 0){
                //data
			    strokeViewListener.currentStroke.points.push({ x: ev._x, y: ev._y });
                //UI
                context.lineTo(ev._x,ev._y);
                context.stroke();
            }
        }
    };
    this.mouseup = function (ev) {
        if(strokeViewListener.started){
			//data
			strokeViewListener.strokesHistory.strokes.push(strokeViewListener.currentStroke);
			strokeViewListener.currentStroke = { points: [] };
            strokeViewListener.idx = 0;
        }
        strokeViewListener.started = false;
    };
	this.mouseout = this.mouseup;
	this.touchstart = this.mousedown;
	this.touchmove = this.mousemove;
	this.touchend = this.mouseup;
	this.touchcancel = this.mouseup;
}

//canvas event proxy
function ev_canvas(ev){
    ev.preventDefault();
    var touches = ev.changedTouches;
    if(touches){
        var touch = touches[0]
        ev._x = touch.pageX-touch.target.offsetLeft;
        ev._y = touch.pageY-touch.target.offsetTop;
    }else{
        ev._x = ev.offsetX;
        ev._y = ev.offsetY;
    }
    var func = strokeViewListener[ev.type];
    if (func) {
      func(ev);
    }
}
