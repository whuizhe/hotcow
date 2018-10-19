/**
 * Created by wanghuizhe on 16/6/1.
 */

var dictd = document.getElementById("dict").value;
var obj = JSON.parse(dictd);

var graph = new Springy.Graph();

var domaind = graph.newNode({
  label: obj.domaind,
  ondoubleclick: function() { console.log("Hello!"); }
});

//赋值
var out_add = graph.newNode({label: obj.out_add});

if (obj.dmz != 0) {
    var dmz = graph.newNode({label: obj.dmz});
    if (obj.dmz_real != 0) {
        var dmz_real = graph.newNode({label: obj.dmz_real});
    }
}

if (obj.proxy != 0) {
    var proxy = graph.newNode({label: obj.proxy});
    if (obj.proxy_real != 0) {
        var proxy_real = graph.newNode({label: obj.proxy_real});
    }
}

if (obj.hard != 0) {
    var hard = graph.newNode({label: obj.hard});
    if (obj.hard_real != 0) {
        var hard_real = graph.newNode({label: obj.hard_real});
    }
}

if (obj.soft1 != 0) {
    var soft1 = graph.newNode({label: obj.soft1});
    if (obj.soft_real41 != 0) {
        var soft_real41 = graph.newNode({label: obj.soft_real41});
    }
}

if (obj.soft2 != 0) {
    var soft2 = graph.newNode({label: obj.soft2});
    if (obj.soft_real42 != 0) {
        var soft_real42 = graph.newNode({label: obj.soft_real42});
    }
}

if (obj.soft3 != 0) {
    var soft3 = graph.newNode({label: obj.soft3});
    if (obj.soft_real43 != 0) {
        var soft_real43 = graph.newNode({label: obj.soft_real43});
    }
}

if (obj.soft4 != 0) {
    var soft4 = graph.newNode({label: obj.soft4});
    if (obj.soft_real44 != 0) {
        var soft_real44 = graph.newNode({label: obj.soft_real44});
    }
}

if (obj.soft5 != 0) {
    var soft5 = graph.newNode({label: obj.soft5});
    if (obj.soft_real45 != 0) {
        var soft_real45 = graph.newNode({label: obj.soft_real45});
    }
}


//赋关系
graph.newEdge(domaind, out_add, {color: '#00A0B0'});
//dmz
if (obj.dmz != 0) {
    graph.newEdge(out_add, dmz, {color: '#FF0000'});
        if (obj.dmz_real != 0) {
            graph.newEdge(dmz, dmz_real, {color: '#25D7DA'});
        }
    //反向代理判断
        if (obj.proxy != 0) {
            graph.newEdge(dmz, proxy, {color: '#25D7DA'});
            if (obj.proxy_real != 0) {
                graph.newEdge(proxy, proxy_real, {color: '#2585DA'});
            }
        if (obj.hard != 0) {
            graph.newEdge(proxy, hard, {color: '#2585DA'});
            if (obj.hard_real != 0) {
                graph.newEdge(hard, hard_real, {color: '#E71867'});
            }


            if (obj.soft1 != 0) {
                graph.newEdge(hard, soft1, {color: '#E71867'});
                if (obj.soft_real41 != 0) {
                    graph.newEdge(soft1, soft_real41, {color: '#04B29F'});
                }
            }

            if (obj.soft2 != 0) {
                graph.newEdge(hard, soft2, {color: '#E71867'});
                if (obj.soft_real42 != 0) {
                    graph.newEdge(soft2, soft_real42, {color: '#04B29F'});
                }
            }

            if (obj.soft3 != 0) {
                graph.newEdge(hard, soft3, {color: '#E71867'});
                if (obj.soft_real43 != 0) {
                    graph.newEdge(soft3, soft_real43, {color: '#04B29F'});
                }
            }

            if (obj.soft4 != 0) {
                graph.newEdge(hard, soft4, {color: '#E71867'});
                if (obj.soft_real44 != 0) {
                    graph.newEdge(soft4, soft_real44, {color: '#04B29F'});
                }
            }

            if (obj.soft5 != 0) {
                graph.newEdge(hard, soft5, {color: '#E71867'});
                if (obj.soft_real45 != 0) {
                    graph.newEdge(soft5, soft_real45, {color: '#04B29F'});
                }
            }
        }
        else if (obj.soft1 != 0) {
                graph.newEdge(proxy, soft1, {color: '#E71867'});
                if (obj.soft_real41 != 0) {
                    graph.newEdge(soft1, soft_real41, {color: '#04B29F'});
                }
            }

            if (obj.soft2 != 0) {
                graph.newEdge(proxy, soft2, {color: '#E71867'});
                if (obj.soft_real42 != 0) {
                    graph.newEdge(soft2, soft_real42, {color: '#04B29F'});
                }
            }

            if (obj.soft3 != 0) {
                graph.newEdge(proxy, soft3, {color: '#E71867'});
                if (obj.soft_real43 != 0) {
                    graph.newEdge(soft3, soft_real43, {color: '#04B29F'});
                }
            }

            if (obj.soft4 != 0) {
                graph.newEdge(proxy, soft4, {color: '#E71867'});
                if (obj.soft_real44 != 0) {
                    graph.newEdge(soft4, soft_real44, {color: '#04B29F'});
                }
            }

            if (obj.soft5 != 0) {
                graph.newEdge(proxy, soft5, {color: '#E71867'});
                if (obj.soft_real45 != 0) {
                    graph.newEdge(soft5, soft_real45, {color: '#04B29F'});
                }
            }

        }
    //硬负载代理判断
        else if (obj.hard != 0) {
            graph.newEdge(dmz, hard, {color: '#25D7DA'});
            if (obj.hard_real != 0) {
                graph.newEdge(hard, hard_real, {color: '#E71867'});
            }
        if (obj.soft1 != 0) {
            graph.newEdge(hard, soft1, {color: '#E71867'});
            if (obj.soft_real41 != 0) {
                graph.newEdge(soft1, soft_real41, {color: '#04B29F'});
            }
        }

        if (obj.soft2 != 0) {
            graph.newEdge(hard, soft2, {color: '#E71867'});
            if (obj.soft_real42 != 0) {
                graph.newEdge(soft2, soft_real42, {color: '#04B29F'});
            }
        }

        if (obj.soft3 != 0) {
            graph.newEdge(hard, soft3, {color: '#E71867'});
            if (obj.soft_real43 != 0) {
                graph.newEdge(soft3, soft_real43, {color: '#04B29F'});
            }
        }

        if (obj.soft4 != 0) {
            graph.newEdge(hard, soft4, {color: '#E71867'});
            if (obj.soft_real44 != 0) {
                graph.newEdge(soft4, soft_real44, {color: '#04B29F'});
            }
        }

        if (obj.soft5 != 0) {
            graph.newEdge(hard, soft5, {color: '#E71867'});
            if (obj.soft_real45 != 0) {
                graph.newEdge(soft5, soft_real45, {color: '#04B29F'});
            }
        }
    //软负载判断
        }
        else if (obj.soft1 != 0) {
            graph.newEdge(dmz, soft1, {color: '#25D7DA'});
            if (obj.soft_real41 != 0) {
                graph.newEdge(soft1, soft_real41, {color: '#04B29F'});
            }
        if (obj.soft2 != 0) {
            graph.newEdge(dmz, soft2, {color: '#25D7DA'});
            if (obj.soft_real42 != 0) {
                graph.newEdge(soft2, soft_real42, {color: '#04B29F'});
            }
        }

        if (obj.soft3 != 0) {
            graph.newEdge(dmz, soft3, {color: '#25D7DA'});
            if (obj.soft_real43 != 0) {
                graph.newEdge(soft3, soft_real43, {color: '#04B29F'});
            }
        }

        if (obj.soft4 != 0) {
            graph.newEdge(dmz, soft4, {color: '#25D7DA'});
            if (obj.soft_real44 != 0) {
                graph.newEdge(soft4, soft_real44, {color: '#04B29F'});
            }
        }

        if (obj.soft5 != 0) {
            graph.newEdge(dmz, soft5, {color: '#25D7DA'});
            if (obj.soft_real45 != 0) {
                graph.newEdge(soft5, soft_real45, {color: '#04B29F'});
            }
        }
        }

}
//反向代理
else if (obj.proxy != 0) {
    //反向代理判断
    graph.newEdge(out_add, proxy, {color: '#00DB00'});
        if (obj.proxy_real != 0) {
            graph.newEdge(proxy, proxy_real, {color: '#2585DA'});
            }
        if (obj.hard != 0) {
            graph.newEdge(proxy, hard, {color: '#2585DA'});
            if (obj.hard_real != 0) {
                graph.newEdge(hard, hard_real, {color: '#E71867'});
            }

            if (obj.soft1 != 0) {
                graph.newEdge(hard, soft1, {color: '#E71867'});
                if (obj.soft_real41 != 0) {
                    graph.newEdge(soft1, soft_real41, {color: '#04B29F'});
                }
            }

            if (obj.soft2 != 0) {
                graph.newEdge(hard, soft2, {color: '#E71867'});
                if (obj.soft_real42 != 0) {
                    graph.newEdge(soft2, soft_real42, {color: '#04B29F'});
                }
            }

            if (obj.soft3 != 0) {
                graph.newEdge(hard, soft3, {color: '#E71867'});
                if (obj.soft_real43 != 0) {
                    graph.newEdge(soft3, soft_real43, {color: '#04B29F'});
                }
            }

            if (obj.soft4 != 0) {
                graph.newEdge(hard, soft4, {color: '#E71867'});
                if (obj.soft_real44 != 0) {
                    graph.newEdge(soft4, soft_real44, {color: '#04B29F'});
                }
            }

            if (obj.soft5 != 0) {
                graph.newEdge(hard, soft5, {color: '#E71867'});
                if (obj.soft_real45 != 0) {
                    graph.newEdge(soft5, soft_real45, {color: '#04B29F'});
                }
            }
        }
    //硬负载代理判断
        else if (obj.hard != 0) {
            graph.newEdge(dmz, hard, {color: '#25D7DA'});
            if (obj.hard_real != 0) {
                graph.newEdge(hard, hard_real, {color: '#E71867'});
            }
        if (obj.soft1 != 0) {
            graph.newEdge(hard, soft1, {color: '#E71867'});
            if (obj.soft_real41 != 0) {
                graph.newEdge(soft1, soft_real41, {color: '#04B29F'});
            }
        }

        if (obj.soft2 != 0) {
            graph.newEdge(hard, soft2, {color: '#E71867'});
            if (obj.soft_real42 != 0) {
                graph.newEdge(soft2, soft_real42, {color: '#04B29F'});
            }
        }

        if (obj.soft3 != 0) {
            graph.newEdge(hard, soft3, {color: '#E71867'});
            if (obj.soft_real43 != 0) {
                graph.newEdge(soft3, soft_real43, {color: '#04B29F'});
            }
        }

        if (obj.soft4 != 0) {
            graph.newEdge(hard, soft4, {color: '#E71867'});
            if (obj.soft_real44 != 0) {
                graph.newEdge(soft4, soft_real44, {color: '#04B29F'});
            }
        }

        if (obj.soft5 != 0) {
            graph.newEdge(hard, soft5, {color: '#E71867'});
            if (obj.soft_real45 != 0) {
                graph.newEdge(soft5, soft_real45, {color: '#04B29F'});
            }
        }
    //软负载判断
        }
        else if (obj.soft1 != 0) {
            graph.newEdge(dmz, soft1, {color: '#25D7DA'});
            if (obj.soft_real41 != 0) {
                graph.newEdge(soft1, soft_real41, {color: '#04B29F'});
            }
        if (obj.soft2 != 0) {
            graph.newEdge(dmz, soft2, {color: '#25D7DA'});
            if (obj.soft_real42 != 0) {
                graph.newEdge(soft2, soft_real42, {color: '#04B29F'});
            }
        }

        if (obj.soft3 != 0) {
            graph.newEdge(dmz, soft3, {color: '#25D7DA'});
            if (obj.soft_real43 != 0) {
                graph.newEdge(soft3, soft_real43, {color: '#04B29F'});
            }
        }

        if (obj.soft4 != 0) {
            graph.newEdge(dmz, soft4, {color: '#25D7DA'});
            if (obj.soft_real44 != 0) {
                graph.newEdge(soft4, soft_real44, {color: '#04B29F'});
            }
        }

        if (obj.soft5 != 0) {
            graph.newEdge(dmz, soft5, {color: '#25D7DA'});
            if (obj.soft_real45 != 0) {
                graph.newEdge(soft5, soft_real45, {color: '#04B29F'});
            }
        }
        }

}
//硬负载
else if (obj.hard != 0) {
    graph.newEdge(out_add, hard, {color: '#0080FF'});
            if (obj.hard_real != 0) {
                graph.newEdge(hard, hard_real, {color: '#E71867'});
            }

            if (obj.soft1 != 0) {
                graph.newEdge(hard, soft1, {color: '#E71867'});
                if (obj.soft_real41 != 0) {
                    graph.newEdge(soft1, soft_real41, {color: '#04B29F'});
                }
            }

            if (obj.soft2 != 0) {
                graph.newEdge(hard, soft2, {color: '#E71867'});
                if (obj.soft_real42 != 0) {
                    graph.newEdge(soft2, soft_real42, {color: '#04B29F'});
                }
            }

            if (obj.soft3 != 0) {
                graph.newEdge(hard, soft3, {color: '#E71867'});
                if (obj.soft_real43 != 0) {
                    graph.newEdge(soft3, soft_real43, {color: '#04B29F'});
                }
            }

            if (obj.soft4 != 0) {
                graph.newEdge(hard, soft4, {color: '#E71867'});
                if (obj.soft_real44 != 0) {
                    graph.newEdge(soft4, soft_real44, {color: '#04B29F'});
                }
            }

            if (obj.soft5 != 0) {
                graph.newEdge(hard, soft5, {color: '#E71867'});
                if (obj.soft_real45 != 0) {
                    graph.newEdge(soft5, soft_real45, {color: '#04B29F'});
                }
            }
}
//软负载
else if (obj.soft1 != 0) {
        graph.newEdge(out_add, soft1, {color: '#F75000'});
        if (obj.soft_real41 != 0) {
            graph.newEdge(soft1, soft_real41, {color: '#04B29F'});
        }

            if (obj.soft2 != 0) {
                graph.newEdge(out_add, soft2, {color: '#F75000'});
                if (obj.soft_real42 != 0) {
                    graph.newEdge(soft2, soft_real42, {color: '#04B29F'});
                }
            }

            if (obj.soft3 != 0) {
                graph.newEdge(out_add, soft3, {color: '#F75000'});
                if (obj.soft_real43 != 0) {
                    graph.newEdge(soft3, soft_real43, {color: '#04B29F'});
                }
            }

            if (obj.soft4 != 0) {
                graph.newEdge(out_add, soft4, {color: '#F75000'});
                if (obj.soft_real44 != 0) {
                    graph.newEdge(soft4, soft_real44, {color: '#04B29F'});
                }
            }

            if (obj.soft5 != 0) {
                graph.newEdge(out_add, soft5, {color: '#F75000'});
                if (obj.soft_real45 != 0) {
                    graph.newEdge(soft5, soft_real45, {color: '#04B29F'});
                }
            }
}

jQuery(function(){
  var springy = window.springy = jQuery('#springydemo').springy({
    graph: graph,
    nodeSelected: function(node){
      console.log('Node selected: ' + JSON.stringify(node.data));
    }
  });
});
