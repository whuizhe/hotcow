$(document).ready(function(){
    $("#login_btn").on('click', function(e){
        e.preventDefault();
        var user = $("input[name='email']").val();
        var psd = $("input[name='password']").val();
        if(user.trim()=='' || psd.trim()==''){
            swal('邮箱和密码不能为空！','','error');
            return false;
        }
        $.ajax({
            url: '/login/logtok/?email='+user,
            type: 'get',
            success:function(res){
                if(!res.Token){
                    $('#login_error').text('用户不存在！');
                    return false;
                }
                var key = res.Token;
                var s1 = encrypt(psd, key);
                $.ajax({
                    url: '',
                    data: {
                        email: user,
                        password: s1
                    },
                    type: 'post',
                    dataType: 'json',
                    success: function(res){
                        if(!res.list){
                            var next = res.next?res.next:'';
                            window.location.href = next;
                        }
                        else{
                            $('#login_error').text(res.list);
                        }
                    },
                    error: function(){
                        $('#login_error').text('登录失败！');
                    }
                });
            },
            error: function(){
                $('#login_error').text('用户不存在！');
                return false;
            }
        })
        
        return false;
    })
    function encrypt(str,key){
            
        var str = str;
        // 密钥 16 位
        var key = key;
        // 初始向量 initial vector 16 位
        var iv = key;
        // key 和 iv 可以一致
        
        key = CryptoJS.enc.Utf8.parse(key);
        iv = CryptoJS.enc.Utf8.parse(iv);
        
        var encrypted = CryptoJS.AES.encrypt(str, key, {
            iv: iv,
            mode: CryptoJS.mode.CBC,
            padding: CryptoJS.pad.Pkcs7 
        });
        
        // 转换为字符串
        encrypted = encrypted.ciphertext.toString();
        return encrypted;
    }
})