var d3 = require('d3');

function Tree(opts) {
    //load in arguments from config object
    this.element = opts.element;
    if (opts.margin === undefined) {
        this.margin = {
            top: 20,
            right: 120,
            bottom: 20,
            left: 120
        };
    } else {
        this.margin = opts.margin;
    }
    this.height = opts.height || 800 - this.margin.top - this.margin.bottom;
    this.width = opts.width || 960 - this.margin.right - this.margin.left;
    this.i = 0;
    this.duration = 750;

    this.tree = d3.layout.tree()
        .size([this.height, this.width]);

    this.svg = d3.select(this.element).append('svg')
        .attr('width', this.width + this.margin.left + this.margin.right)
        .attr('height', this.height + this.margin.top + this.margin.bottom)
        .append('g')
        .attr('transform', 'translate(' + this.margin.left + ',' + this.margin.top + ')');
}

Tree.prototype.diagonal = d3.svg.diagonal()
    .projection(function(d) {
        return [d.y, d.x];
    });

Tree.prototype.setData = function(data) {
    this.root = data;
    this.root.x0 = this.height / 2;
    this.root.y0 = 0;

    // Recursively collapse the tree
    function collapse(node) {
        if (node.children) {
            node._children = node.children;
            node._children.forEach(collapse);
            node.children = null;
        }
    }

    this.root.children.forEach(collapse);
    this.update(this.root);
};

Tree.prototype.getData = function(url) {
    var _this = this;
    d3.json(url, function(error, data) {
        if (error) throw error;

        _this.setData(data);
    });
};

Tree.prototype.update = function(source) {
    var _this = this;

    // Toggle children on click
    function click(d) {
        if (d.children) {
            d._children = d.children;
            d.children = null;
        } else {
            d.children = d._children;
            d._children = null;
        }
        _this.update(d);
    }

    // Compute new tree layout
    var nodes = this.tree.nodes(this.root).reverse(),
        links = this.tree.links(nodes);

    // Normalize for fixed-depth
    nodes.forEach(function(d) {
        d.y = d.depth * 180;
    });

    // Update the nodes
    var node = this.svg.selectAll("g.node")
        .data(nodes, function(d) {
            return d.id || (d.id = ++_this.i);
        });

    // Enter any new nodes at the parent's previous position
    var nodeEnter = node.enter().append('g')
        .attr('class', 'node')
        .attr('transform', function(d) {
            return 'translate(' + source.y0 + ',' + source.x0 + ')';
        })
        .on('click', click);

    nodeEnter.append('circle')
        .attr('r', 1e-6)
        .style('fill', function(d) {
            return d._children ? 'lightstellblue' : '#fff';
        });

    nodeEnter.append('text')
        .attr('x', function(d) {
            return d.children || d._children ? -10 : 10;
        })
        .attr('dy', '.35em')
        .attr('text-anchor', function(d) {
            return d.children || d._children ? "end" : "start";
        })
        .text(function(d) {
            return d.name;
        })
        .style('fill-opacity', 1e-6);

    // Transition nodes to their new postition
    var nodeUpdate = node.transition()
        .duration(this.duration)
        .attr('transform', function(d) {
            return 'translate(' + d.y + ',' + d.x + ')';
        });

    nodeUpdate.select('circle')
        .attr('r', 4.5)
        .style('fill', function(d) {
            return d._children ? 'lightsteelblue' : '#fff';
        });

    nodeUpdate.select('text')
        .style('fill-opacity', 1);

    // Transition exiting nodes to the parent's new position.
    var nodeExit = node.exit().transition()
        .duration(this.duration)
        .attr("transform", function(d) {
            return "translate(" + source.y + "," + source.x + ")";
        })
        .remove();

    nodeExit.select("circle")
        .attr("r", 1e-6);

    nodeExit.select("text")
        .style("fill-opacity", 1e-6);

    // Update the links…
    var link = this.svg.selectAll("path.link")
        .data(links, function(d) {
            return d.target.id;
        });

    // Enter any new links at the parent's previous position.
    link.enter().insert("path", "g")
        .attr("class", "link")
        .attr("d", function(d) {
            var o = {
                x: source.x0,
                y: source.y0
            };
            return _this.diagonal({
                source: o,
                target: o
            });
        });

    // Transition links to their new position.
    link.transition()
        .duration(this.duration)
        .attr("d", this.diagonal);

    // Transition exiting nodes to the parent's new position.
    link.exit().transition()
        .duration(this.duration)
        .attr("d", function(d) {
            var o = {
                x: source.x,
                y: source.y
            };
            return _this.diagonal({
                source: o,
                target: o
            });
        })
        .remove();

    // Stash the old positions for transition.
    nodes.forEach(function(d) {
        d.x0 = d.x;
        d.y0 = d.y;
    });
};

module.exports = Tree;
