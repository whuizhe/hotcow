/**
 * Created by WangZehua on 16/12/8.
 */


 (function(win){
    var _window = win;
/*
复制剪切板
obj{
    elements: 需要初始化的元素
    url: 数据请求url
    key: 数据的关键字
    callback_success: copy成功后的回调函数
    callback_fail: copy失败后的回调函数
}
*/
 	_window.initCopyToClipbord= function(obj){
            var _obj = obj;
            $('body').on('click', _obj.elements, function(){
                var ipt = document.createElement("input");
                ipt.style.position = 'fixed';
                ipt.style.top = 0;
                ipt.style.left = 0;
                ipt.style.border = 'none';
                ipt.style.outline = 'none';
                ipt.style.resize = 'none';
                ipt.style.background = 'transparent';
                ipt.style.color = 'transparent';
                ipt.zIndex = 1000;
                var _this = this;
                var success;
                var data;
                if(_obj.url && typeof(_obj.url)=='function'){
                    url = _obj.url.call(_this);
                }
                else{
                    url = _obj.url?_obj.url + _this.getAttribute('data-id'):$(_this).attr('url') + _this.getAttribute('data-id')
                }
                $.ajax({
                    type:'get', 
                    url:url,
                    async:false,
                    timeout:6000,
                    success:function (res) {
                        data = res;
                    },
                    error:function(){
                        data = null;
                    }
                });
                if(!data || !data.status){
                    success = false;
                }
                else{
                    ipt.value = data[_obj.key?_obj.key:$(_this).attr('key')];
                    document.body.appendChild(ipt);
                    ipt.focus();
                    ipt.select();
                    try {
                        success = document.execCommand('copy');
                    } catch (err) {
                        success = false;
                    }
                    document.body.removeChild(ipt);
                }
                success?_obj.callback_success(_this,data):_obj.callback_fail(_this,data);
                
            })
 		}
         _window.copyToClipbord =function(obj){
            var _obj = obj;
            $('body').on('click', _obj.elements, function(){
                var ipt = document.createElement("input");
                ipt.style.position = 'fixed';
                ipt.style.top = 0;
                ipt.style.left = 0;
                ipt.style.border = 'none';
                ipt.style.outline = 'none';
                ipt.style.resize = 'none';
                ipt.style.background = 'transparent';
                ipt.style.color = 'transparent';
                ipt.zIndex = 1000;
                var _this = this;
                var success;
                var data;
                ipt.value = $(this).attr('copy-val');
                document.body.appendChild(ipt);
                ipt.focus();
                ipt.select();
                try {
                    success = document.execCommand('copy');
                } catch (err) {
                    success = false;
                }
                document.body.removeChild(ipt);
                if(obj.callback){
                    obj.callback.call(_this);
                }
            })
         }
         _window.isValidIP = function(ip){ 
            var reg =  /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/     
            return reg.test(ip);
        }    
    _window.showSysList = function(cl){
        var cl = cl?cl:'.showSysList';
        $('body').on('click', cl, function(e){
            e.preventDefault();
            var url = this.href;
            layer.open({
                type: 2,
                title: '',
                shadeClose: true,
                shade: 0.8,
                area: ['1000px', '600px'],
                content: url
            })
        })
    }
// 对Date的扩展，将 Date 转化为指定格式的String   
// 月(M)、日(d)、小时(h)、分(m)、秒(s)、季度(q) 可以用 1-2 个占位符，   
// 年(y)可以用 1-4 个占位符，毫秒(S)只能用 1 个占位符(是 1-3 位的数字)   
// 例子：   
// (new Date()).Format("yyyy-MM-dd hh:mm:ss.S") ==> 2006-07-02 08:09:04.423   
// (new Date()).Format("yyyy-M-d h:m:s.S")      ==> 2006-7-2 8:9:4.18   
    Date.prototype.Format = function(fmt)   
    { //author: meizz   
      var o = {   
        "M+" : this.getMonth()+1,                 //月份   
        "d+" : this.getDate(),                    //日   
        "h+" : this.getHours(),                   //小时   
        "m+" : this.getMinutes(),                 //分   
        "s+" : this.getSeconds(),                 //秒   
        "q+" : Math.floor((this.getMonth()+3)/3), //季度   
        "S"  : this.getMilliseconds()             //毫秒   
      };   
      if(/(y+)/.test(fmt))   
        fmt=fmt.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));   
      for(var k in o)   
        if(new RegExp("("+ k +")").test(fmt))   
      fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));   
      return fmt;   
    }
//手机号验证
    _window.isPhoneNum = function(phoneNum){
        var reg = /^1[3|4|5|7|8][0-9]{9}$/; //验证规则
        return reg.test(phoneNum); //true
    }
/*
 获取环境数据
*/
    _window.getEnvSelectOption = function(obj){
         return $.get('/server/ipenv', function(res){
            if(res){
                if(obj){
                    var value = obj.val();
                    var h = '';
                    for(var i in res){
                        h+='<option value='+res[i]+'>'+res[i]+'</option>';
                    }
                    obj.html(h);
                    obj.val(value);
                }
            }
            else{
                console.error('Can not get enviroment select options!');
            }
        })
    }
/*
表格函数
*/
    _window.table = function(data,table,drawCallback,options){
        if(data){
            this.data = data;
        }
        if(table){
            this.stable = table;
        }
        if(drawCallback){
            this.drawcallback = drawCallback;
        }
        if(options){
            this.options = options;
        }
        return this;
    }
    table.prototype.createThead = function(){
        var _this = this;
        var title = _this.data.title;
        var tr = $('<tr></tr>');
        if(!title || title.length==0){
            return false;
        }
        for(var x in title){
            if(title[x][0]=='bus_ip'){
                var th = '<th name="'+title[x][0]+'" data-priority="1">'+title[x][1]+'</th>';  
            }
            else{
                var th = '<th name="'+title[x][0]+'">'+title[x][1]+'</th>';    
            }
            tr.append(th);
        }
        return tr;
    }
    table.prototype.createDataArr = function(itemData){
        var _this = this;
        var _itemData = itemData;
        var title = _this.data.title;
        var arr = [];
        var id = _itemData.id?_itemData.id:'';
        for(var x in title){
            var name = title[x][0];
            var html = '';
            var val = _itemData[name];
            switch(name){
                case 'operation':
                    if(data['next_time']!=''){
                        html+='<a href="/automation/crontabedit/'+id+'" class="edit_btn"><i class="fa fa-edit"></i></a>'
                    }
                    html+='<a href="/automation/crontablog/'+id+'" class="log_btn"><i class="fa fa-file-text-o"></i></a>';
                    html+='<a href="/automation/crontabdel/'+id+'" class="delete_btn" type="button"><i class="fa fa-trash"></i></a>';
                    break;
                case 'run_type':
                    if(val=='interval'){
                        html = '固定间隔';
                    }
                    else if(val=='date'){
                        html = '一次性任务';
                    }
                    else{
                        html = '固定时间';
                    }
                    break;
                case 'next_time':
                    if(!_this.data.aps_dict){
                        html = '';
                        break;
                    }
                    var s = _this.data.aps_dict[id];
                    if(!s || s=='' || s.length==0){
                        html = '<del>任务已结束</del>';
                    }
                    else{
                        html = s;
                    }
                    break;
                case 'status':
                    if(val==1){
                        html = '<button class="btn btn-primary btn-xs cronstatus">运行</button>';
                    }
                    else if(val==0){
                        html = '<button class="btn btn-warning btn-xs cronstatus">暂停</button>';
                    }
                    else{
                        html = '<button class="btn btn-danger btn-xs">停止</button>';
                    }
                    break;
                default:
                    html = val?val:'';
                    break;
            }
            arr.push(html);
        }
        return arr;
    }
    table.prototype.createTbodyData = function(){
        var _this = this;
        if(!_this.data || !_this.data.param){
            console.error('no data');
            return false;
        }
        var tbody = [];
        for(var i in _this.data.param){
            var item = _this.createDataArr(_this.data.param[i]);
            if(item){
                tbody.push(item);
            }
        }
        return tbody;    
    }
    table.prototype.initTable = function(){
        var _this = this;
        var head = this.createThead();
        if(!head){
            return false;
        }
        this.stable.find('thead').append(head);
        var tbody = this.createTbodyData();
        this.dtable = this.stable.DataTable({
            processing: _this.options&&_this.options.processing?_this.options.processing:true,
            responsive: _this.options&&_this.options.responsive?_this.options.responsive:true,
            responsive:false,
            data: tbody,
            searching: true,
            search: {
                regex: false,
                smart: false,
                caseInsensitive: false
            },
            columnDefs: _this.options&&_this.options.columnDefs?_this.options.columnDefs:[],
            order: _this.options&&_this.options.order?_this.options.order:[],
            dom: '<"html5buttons"B>lTfgitp',
            buttons: [
                { extend: 'copy'},
                {  extend: 'excel', title: 'ExampleFile'},
                {   
                    extend: 'print',
                    customize: function (win){
                            $(win.document.body).addClass('white-bg');
                            $(win.document.body).css('font-size', '10px');
                            $(win.document.body).find('table')
                                    .addClass('compact')
                                    .css('font-size', 'inherit');
                    },
                    exportOptions: {
                        stripHtml: false,
                        format: {
                            body: function ( inner, coldex, rowdex ) {
                                if (inner.length == 0) return inner;
                                var el = $.parseHTML(inner);
                                var result='';
                                $.each( el, function (index, item) {
                                    if (item.nodeName == '#text') result = result + item.textContent;
                                    else if (item.nodeName == 'SUP') result = result + item.outerHTML;
                                    else if (item.nodeName == 'STRONG') result = result + item.outerHTML;
                                    else if (item.nodeName == 'IMG') result = result + item.outerHTML;
                                    else result = result + item.innerText;
                                });
                                return result;
                            }
                        }
                    }
                }
            ],
            drawCallback: _this.drawcallback?function(){_this.drawcallback()}:function(){}
        });
        if(!this.searchIput){
            var ipt = $('<input type="text" id="special_input" class="search form-control input-sm">');
            this.searchIput = ipt;
            this.stable.prevAll('.dataTables_filter').find('input').remove();
            this.stable.prevAll('.dataTables_filter').append(ipt);
            var inputnum = 0;
            ipt.on('input', function(e){
                inputnum ++;
                (function(time){
                    setTimeout(function(){
                        if(time==inputnum){
                            _this.dtable.draw();
                        }
                    },500)
                })(inputnum)
            })
            $.fn.dataTable.ext.search.push(function( settings, data, dataIndex ) {
                var val = ipt.val().toLowerCase(); 
                var reg = new RegExp(val,'g');
                var match = false;
                data.forEach(function(info) {
                    if(reg.test(info.toLowerCase())){
                        match = true;
                        return;
                    }
                }, this);
                if(match){
                    return true;
                }
                else{
                    return false;
                }
            })
        }
        else{
            this.stable.prevAll('.dataTables_filter').find('input').remove();
            this.stable.prevAll('.dataTables_filter').append(this.searchIput);
            this.searchIput.val('');
            this.dtable.draw();
        }
        
        return this.dtable;
    }
//生成环境按钮
    _window.createSubTitle = function(env,name,url){
        var html = '';
        if(env.length==0 || !env){
            return false;
        }
        for(var i in env){
            if(env[i][1][1]){
                html += '<a class="get_content btn btn-primary btn-outline" name="'+name+'" href="'+url+env[i][0]+'" envid="'+env[i][0]+'"><i class="env_item_num">'+env[i][1][1]+'</i>'+env[i][1][0]+'</a>';
            }
            else{
                html += '<a class="get_content btn btn-gray disabled" name="'+name+'" href="'+url+env[i][0]+'" envid="'+env[i][0]+'"><i class="env_item_num">0</i>'+env[i][1][0]+'</a>';
            }
        }
        $('.subtitle_box').html(html);
        return html;
    }
 //根据环境动态改变表格
    _window.getEnvPage = function(mytable,changeItems,callback){
        $('.subtitle_box').on('click','.get_content', function(e){
            e.preventDefault();
            var _this = this;
            if($(this).hasClass('disabled')){
                return false;
            }
            var url = this.href;
            var exActive = $(this).siblings().not('.disabled').not('.btn-outline');
            $(this).siblings().not('.disabled').addClass('btn-outline');
            $(this).removeClass('btn-outline');
            var name = this.name;
            $.ajax({
                url: url,
                type:'get',
                headers:{
                    'BL-Token':'d5269a33-bbc7-'+name+'-a7c4-ee897bf8631f'
                },
                success:function(res){
                    if(res.error){
                        swal(res.error.toString(),'','error');
                        if(res.error==401){
                            $(_this).remove();
                        }
                        exActive.removeClass('btn-outline');
                        return false;
                    }
                    for(var i in changeItems){
                        mytable.data[i]= res[changeItems[i]];
                    }
                    if(mytable.data.button && mytable.data.button.add){
                        $('.add_btn').show();
                    }
                    else if(mytable.data.button && !mytable.data.button.add){
                        $('.add_btn').hide();
                    }
                    if(callback){
                        callback(res);
                    }
                    if(mytable.dtable){
                        mytable.dtable.destroy();
                        if(mytable.stable.parent().length==0){
                            $(".ibox-content").append(mytable.stable);
                        }
                        $('thead').html('');
                        $('tbody').html('');
                    }
                    mytable.initTable(); 
                    
                },
                complete: function(xml){
                    var _this = this;
                    var header = xml.getResponseHeader('content-type');
                    var link = xml.getResponseHeader('link');
                    if(header.indexOf('html')>-1){
                        var html = xml.responseText;
                        if(html.search('401')>-1){
                            if(swal){
                                swal('无访问权限!','','error');
                            }
                            else{
                                alert('无访问权限!');
                            }
                        }   
                        else if(html.search('404')>-1){
                            if(swal){
                                swal('页面不存在!','','error');
                            }
                            else{
                                alert('页面不存在!');
                            }
                        }
                        else{
                            window.location.reload();
                        }
                    }
                }
            })
        })
    }
//密码格式验证
    _window.isPasswd = function(s)  
    {  
        // var patrn=/^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,15}$/;
        // if (!patrn.exec(s)){
        //     return false;
        // }
        // else{
        //     p2  = /[^\da-zA-Z\+\-\_@$]/;
        //     if(p2.exec(s)){
        //         return false;
        //     }
        // }
        if (s.length<6 || s.length>15){
            return false;
        }
        return true;
    } 
//克隆对象
    _window.cloneObj = function(obj) {
        if (null == obj || "object" != typeof obj) return obj;
        var copy = obj.constructor();
        for (var attr in obj) {
            if (obj.hasOwnProperty(attr)) copy[attr] = obj[attr];
        }
        return copy;
    }
    _window.initGroupSelectOptions = function(obj,val){
         $.get('/vps/servergroup',function(res){
             var options = '';
            for(var i in res.servergroup){
                options += '<option value="'+i.trim()+'">'+i+'('+res.servergroup[i]+')</option>';
            }
            obj.append(options);
            if(val){
                obj.val(val);
            }
            obj.select2({
                allowClear: true
            });
        })
    }
    $.ajaxSetup({
        global: true,
        complete: function(xml,txt){
            var _this = this;
            var header = xml.getResponseHeader('content-type');
            var link = xml.getResponseHeader('link');
            if(xml.status && xml.status!=200 && xml.status!=302){
                var text = '出错了';
                switch(xml.status){
                    case 500:
                        text = '服务器内部错误';
                        break;
                    case 502:
                        text = '错误网关';
                        break;
                    case 503:
                        text = '服务器超时';
                        break;
                    case 504:
                        text = '网关超时';
                        break;
                    case 404:
                        text = '请求的网页不存在';
                        break;
                }
                swal(text,xml.status,'error');
                return;
            }
            if(header && header.indexOf('html')>-1){
                var html = xml.responseText;
                if(html.search('jumploginrefreshhtml')>-1){
                    window.location.reload();
                }
            }
        }
    }); 
    $('body').on('change', 'input', function(){
        if($(this).val()!=''){
            $(this).val($(this).val().trim());
        }
    })
    _window.isIP = function(s){
        var pattern=/^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$/;
        if (!pattern.exec(s)) return false;
        return true;
    }
 })(window)