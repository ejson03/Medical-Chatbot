(window.webpackJsonp = window.webpackJsonp || []).push([
   [2],
   {
      28: function (e) {
         e.exports = {
            host: 'localhost',
            port: 9984,
            ws_port: 9985,
            api: '/api/v1/',
            validTx: 'streams/valid_transactions',
            secure: !1
         };
      },
      287: function (e, t, n) {
         'use strict';
         n.r(t);
         var o = n(0),
            r = n.n(o),
            i = n(72),
            a = n.n(i),
            c = n(31),
            l = n(88),
            s = n(282),
            u = (n(538), n(535), n(130)),
            f = n(557),
            p = n(558);
         n(533);
         function h(e) {
            return (h =
               'function' === typeof Symbol && 'symbol' === typeof Symbol.iterator
                  ? function (e) {
                       return typeof e;
                    }
                  : function (e) {
                       return e && 'function' === typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype
                          ? 'symbol'
                          : typeof e;
                    })(e);
         }
         function m(e, t) {
            return (m =
               Object.setPrototypeOf ||
               function (e, t) {
                  return (e.__proto__ = t), e;
               })(e, t);
         }
         function y(e, t) {
            for (var n = 0; n < t.length; n++) {
               var o = t[n];
               (o.enumerable = o.enumerable || !1),
                  (o.configurable = !0),
                  'value' in o && (o.writable = !0),
                  Object.defineProperty(e, o.key, o);
            }
         }
         function d(e, t) {
            return !t || ('object' !== h(t) && 'function' !== typeof t)
               ? (function (e) {
                    if (void 0 === e)
                       throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
                    return e;
                 })(e)
               : t;
         }
         function b(e) {
            return (b =
               Object.getPrototypeOf ||
               function (e) {
                  return e.__proto__;
               })(e);
         }
         var v = (function (e) {
               function t() {
                  return (
                     (function (e, t) {
                        if (!(e instanceof t)) throw new TypeError('Cannot call a class as a function');
                     })(this, t),
                     d(this, b(t).apply(this, arguments))
                  );
               }
               var n, o, i;
               return (
                  (n = t),
                  (o = [
                     {
                        key: 'render',
                        value: function () {
                           return r.a.createElement(
                              f.a,
                              { id: 'appHeader', className: 'App-header', size: 'small' },
                              r.a.createElement(
                                 p.a,
                                 { className: 'logo-item' },
                                 r.a.createElement(
                                    'svg',
                                    { className: 'logo logo--sm logo--white--green', 'aria-labelledby': 'title' },
                                    r.a.createElement('use', { xlinkHref: '/img/logo.svg#logo' })
                                 )
                              )
                           );
                        }
                     }
                  ]) && y(n.prototype, o),
                  i && y(n, i),
                  (function (e, t) {
                     if ('function' !== typeof t && null !== t)
                        throw new TypeError('Super expression must either be null or a function');
                     m(e.prototype, t && t.prototype), t && m(e, t);
                  })(t, e),
                  t
               );
            })(o.Component),
            g = n(556),
            w = n(89);
         n(318);
         function E(e) {
            return (E =
               'function' === typeof Symbol && 'symbol' === typeof Symbol.iterator
                  ? function (e) {
                       return typeof e;
                    }
                  : function (e) {
                       return e && 'function' === typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype
                          ? 'symbol'
                          : typeof e;
                    })(e);
         }
         function k(e, t) {
            return (k =
               Object.setPrototypeOf ||
               function (e, t) {
                  return (e.__proto__ = t), e;
               })(e, t);
         }
         function _(e, t) {
            for (var n = 0; n < t.length; n++) {
               var o = t[n];
               (o.enumerable = o.enumerable || !1),
                  (o.configurable = !0),
                  'value' in o && (o.writable = !0),
                  Object.defineProperty(e, o.key, o);
            }
         }
         function S(e, t) {
            return !t || ('object' !== E(t) && 'function' !== typeof t)
               ? (function (e) {
                    if (void 0 === e)
                       throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
                    return e;
                 })(e)
               : t;
         }
         function x(e) {
            return (x =
               Object.getPrototypeOf ||
               function (e) {
                  return e.__proto__;
               })(e);
         }
         var O = (function (e) {
               function t() {
                  var e, n, o;
                  !(function (e, t) {
                     if (!(e instanceof t)) throw new TypeError('Cannot call a class as a function');
                  })(this, t);
                  for (var r = arguments.length, i = new Array(r), a = 0; a < r; a++) i[a] = arguments[a];
                  return S(o, ((n = o = S(this, (e = x(t)).call.apply(e, [this].concat(i)))), (o.activeIndex = 0), n));
               }
               var n, o, i;
               return (
                  (n = t),
                  (o = [
                     {
                        key: 'render',
                        value: function () {
                           return r.a.createElement(
                              w.a,
                              { inverted: !0, pointing: !0, secondary: !0, size: 'small' },
                              r.a.createElement(
                                 u.a,
                                 { fluid: !0 },
                                 r.a.createElement(w.a.Item, { as: 'div', active: !0 }, this.props.name),
                                 r.a.createElement(
                                    w.a.Item,
                                    { as: 'div' },
                                    'Source:',
                                    r.a.createElement('span', null, this.props.context)
                                 ),
                                 r.a.createElement(
                                    w.a.Item,
                                    { as: 'div' },
                                    'Block Height: ',
                                    r.a.createElement('span', null, this.props.state.lastBlock)
                                 ),
                                 r.a.createElement(
                                    'div',
                                    { className: 'connected' },
                                    r.a.createElement(
                                       w.a.Item,
                                       { as: 'div', className: 'connRight' },
                                       r.a.createElement('span', null, this.props.state.connected)
                                    )
                                 )
                              )
                           );
                        }
                     }
                  ]) && _(n.prototype, o),
                  i && _(n, i),
                  (function (e, t) {
                     if ('function' !== typeof t && null !== t)
                        throw new TypeError('Super expression must either be null or a function');
                     k(e.prototype, t && t.prototype), t && k(e, t);
                  })(t, e),
                  t
               );
            })(o.Component),
            T = n(48),
            C = Object(c.b)(function (e) {
               return { state: e.Stats, context: T.contextName };
            })(O),
            j = function (e, t, n) {
               return { type: 'SET_MODAL', title: e, content: t, open: n };
            },
            N = function (e, t) {
               return { type: 'UPDATE_STATS', connected: e, blockHeight: t };
            },
            B = n(261),
            P = n(28),
            H = (P.secure ? 'https://' : 'http://') + P.host + ':' + P.port + P.api,
            I = new B.Connection(H),
            D = n(90);
         n(306);
         function W(e) {
            return (W =
               'function' === typeof Symbol && 'symbol' === typeof Symbol.iterator
                  ? function (e) {
                       return typeof e;
                    }
                  : function (e) {
                       return e && 'function' === typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype
                          ? 'symbol'
                          : typeof e;
                    })(e);
         }
         function R(e, t) {
            return (R =
               Object.setPrototypeOf ||
               function (e, t) {
                  return (e.__proto__ = t), e;
               })(e, t);
         }
         function A(e, t) {
            for (var n = 0; n < t.length; n++) {
               var o = t[n];
               (o.enumerable = o.enumerable || !1),
                  (o.configurable = !0),
                  'value' in o && (o.writable = !0),
                  Object.defineProperty(e, o.key, o);
            }
         }
         function L(e, t) {
            return !t || ('object' !== W(t) && 'function' !== typeof t)
               ? (function (e) {
                    if (void 0 === e)
                       throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
                    return e;
                 })(e)
               : t;
         }
         function M(e) {
            return (M =
               Object.getPrototypeOf ||
               function (e) {
                  return e.__proto__;
               })(e);
         }
         var J = (function (e) {
               function t() {
                  return (
                     (function (e, t) {
                        if (!(e instanceof t)) throw new TypeError('Cannot call a class as a function');
                     })(this, t),
                     L(this, M(t).apply(this, arguments))
                  );
               }
               var n, o, i;
               return (
                  (n = t),
                  (o = [
                     {
                        key: 'handleClick',
                        value: function () {
                           this.props.onTxClick(this.props.state);
                        }
                     },
                     {
                        key: 'render',
                        value: function () {
                           return r.a.createElement(
                              D.a,
                              {
                                 className: this.props.state.operation.toLowerCase() + ' payloadShadow',
                                 raised: !0,
                                 centered: !0,
                                 onClick: this.handleClick.bind(this)
                              },
                              r.a.createElement(
                                 D.a.Content,
                                 { className: 'cardHeader' },
                                 r.a.createElement(
                                    'span',
                                    { className: 'left floated' },
                                    r.a.createElement('i', { className: 'circle icon' })
                                 ),
                                 r.a.createElement('span', { className: 'right floated trim' }, this.props.txId)
                              ),
                              r.a.createElement(
                                 D.a.Content,
                                 { className: 'cardBody' },
                                 r.a.createElement(D.a.Meta, { className: 'greenColor' }, this.props.state.operation),
                                 r.a.createElement(
                                    D.a.Description,
                                    { className: 'font17' },
                                    'TRANSFER' === this.props.state.operation &&
                                       r.a.createElement(
                                          'div',
                                          null,
                                          r.a.createElement(
                                             'span',
                                             { className: 'left floated upperCase' },
                                             'Asset Id:'
                                          ),
                                          r.a.createElement(
                                             'span',
                                             { className: 'right floated trim' },
                                             this.props.state.asset.id
                                          )
                                       ),
                                    r.a.createElement(
                                       'div',
                                       {
                                          className:
                                             this.props.state.operation.toLowerCase() +
                                             'Desc left floated marginTop4 mb10 wordWrap'
                                       },
                                       this.props.desc
                                    )
                                 )
                              )
                           );
                        }
                     }
                  ]) && A(n.prototype, o),
                  i && A(n, i),
                  (function (e, t) {
                     if ('function' !== typeof t && null !== t)
                        throw new TypeError('Super expression must either be null or a function');
                     R(e.prototype, t && t.prototype), t && R(e, t);
                  })(t, e),
                  t
               );
            })(o.Component),
            z = Object(c.b)(
               function (e, t) {
                  var n = e.Transaction[t.block][t.txId];
                  return {
                     state: n,
                     desc:
                        'CREATE' === n.operation
                           ? JSON.stringify(K('create.description', n))
                           : JSON.stringify(K('transfer.description', n))
                  };
               },
               function (e) {
                  return {
                     onTxClick: function (t) {
                        e(j('Transaction Details', t, !0));
                     }
                  };
               }
            )(J);
         function K(e, t) {
            var n = t;
            return (
               T[e].split('.').map(function (e) {
                  n = n[e];
               }),
               n
            );
         }
         n(304);
         function V(e) {
            return document.getElementById(e).getBoundingClientRect();
         }
         function U(e) {
            return (U =
               'function' === typeof Symbol && 'symbol' === typeof Symbol.iterator
                  ? function (e) {
                       return typeof e;
                    }
                  : function (e) {
                       return e && 'function' === typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype
                          ? 'symbol'
                          : typeof e;
                    })(e);
         }
         function X(e, t) {
            return (X =
               Object.setPrototypeOf ||
               function (e, t) {
                  return (e.__proto__ = t), e;
               })(e, t);
         }
         function F(e, t) {
            for (var n = 0; n < t.length; n++) {
               var o = t[n];
               (o.enumerable = o.enumerable || !1),
                  (o.configurable = !0),
                  'value' in o && (o.writable = !0),
                  Object.defineProperty(e, o.key, o);
            }
         }
         function G(e, t) {
            return !t || ('object' !== U(t) && 'function' !== typeof t)
               ? (function (e) {
                    if (void 0 === e)
                       throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
                    return e;
                 })(e)
               : t;
         }
         function Q(e) {
            return (Q =
               Object.getPrototypeOf ||
               function (e) {
                  return e.__proto__;
               })(e);
         }
         var $ = (function (e) {
               function t() {
                  var e, n, o;
                  !(function (e, t) {
                     if (!(e instanceof t)) throw new TypeError('Cannot call a class as a function');
                  })(this, t);
                  for (var r = arguments.length, i = new Array(r), a = 0; a < r; a++) i[a] = arguments[a];
                  return G(
                     o,
                     ((n = o = G(this, (e = Q(t)).call.apply(e, [this].concat(i)))),
                     (o.maxTxWidth = 324),
                     (o.maxTitleHeight = 20),
                     (o.maxTxHeight = 300),
                     (o.headerHeight = V('appHeader').height),
                     (o.menuHeight = V('dash').height),
                     (o.viewPortHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0)),
                     (o.heightRemainig = o.viewPortHeight - o.headerHeight - o.menuHeight),
                     n)
                  );
               }
               var n, o, i;
               return (
                  (n = t),
                  (o = [
                     {
                        key: 'handleClick',
                        value: function () {
                           this.props.onBlockClick(this.props.block);
                        }
                     },
                     {
                        key: 'render',
                        value: function () {
                           var e = this,
                              t = this.predictBlockSize(),
                              n = { minWidth: t.maxWidth + 'px', maxWidth: t.maxWidth + 'px' },
                              o = { minWidth: t.maxWidth + 'px', maxWidth: t.maxWidth + 'px' };
                           return (
                              (o.maxHeight = t.maxHeight + 'px'),
                              r.a.createElement(
                                 'div',
                                 { className: 'parent' },
                                 r.a.createElement(
                                    'div',
                                    { className: 'blockTitle', style: n, onClick: this.handleClick.bind(this) },
                                    r.a.createElement('span', { id: 'title' }, 'Block'),
                                    r.a.createElement(
                                       'span',
                                       { className: 'blockNo', id: 'title-' + this.props.block },
                                       '#',
                                       this.props.block
                                    )
                                 ),
                                 r.a.createElement(
                                    'div',
                                    { id: this.props.block, style: o, className: 'four wide column bgreen cards box' },
                                    r.a.createElement(
                                       'span',
                                       { id: 'back-' + this.props.block, className: this.props.block + ' dot back' },
                                       this.props.prevBlock && r.a.createElement('div', { className: 'line' })
                                    ),
                                    r.a.createElement('span', {
                                       id: 'front-' + this.props.block,
                                       className: this.props.block + ' dot front'
                                    }),
                                    this.props.state.map(function (t, n) {
                                       return r.a.createElement(z, { key: t, txId: t, block: e.props.block });
                                    })
                                 )
                              )
                           );
                        }
                     },
                     {
                        key: 'predictBlockSize',
                        value: function () {
                           var e = Math.floor(this.heightRemainig / this.maxTxHeight),
                              t = Math.ceil(this.props.state.length / e),
                              n = Math.ceil(this.props.state.length / t) * this.maxTxHeight;
                           return {
                              maxWidth: this.props.state.length < e ? this.maxTxWidth : t * this.maxTxWidth,
                              maxHeight: n
                           };
                        }
                     }
                  ]) && F(n.prototype, o),
                  i && F(n, i),
                  (function (e, t) {
                     if ('function' !== typeof t && null !== t)
                        throw new TypeError('Super expression must either be null or a function');
                     X(e.prototype, t && t.prototype), t && X(e, t);
                  })(t, e),
                  t
               );
            })(o.Component),
            q = Object(c.b)(
               function (e, t) {
                  return e.Transaction[t.block] ? { state: Object.keys(e.Transaction[t.block]) } : { state: [] };
               },
               function (e) {
                  return {
                     onBlockClick: function (t) {
                        var n;
                        ((n = t), I.getBlock(n)).then(function (t) {
                           e(j('Block Details', t, !0));
                        });
                     }
                  };
               }
            )($),
            Y = n(129);
         n(302);
         function Z(e) {
            return (Z =
               'function' === typeof Symbol && 'symbol' === typeof Symbol.iterator
                  ? function (e) {
                       return typeof e;
                    }
                  : function (e) {
                       return e && 'function' === typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype
                          ? 'symbol'
                          : typeof e;
                    })(e);
         }
         function ee(e, t) {
            return (ee =
               Object.setPrototypeOf ||
               function (e, t) {
                  return (e.__proto__ = t), e;
               })(e, t);
         }
         function te(e, t) {
            for (var n = 0; n < t.length; n++) {
               var o = t[n];
               (o.enumerable = o.enumerable || !1),
                  (o.configurable = !0),
                  'value' in o && (o.writable = !0),
                  Object.defineProperty(e, o.key, o);
            }
         }
         function ne(e, t) {
            return !t || ('object' !== Z(t) && 'function' !== typeof t)
               ? (function (e) {
                    if (void 0 === e)
                       throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
                    return e;
                 })(e)
               : t;
         }
         function oe(e) {
            return (oe =
               Object.getPrototypeOf ||
               function (e) {
                  return e.__proto__;
               })(e);
         }
         var re = (function (e) {
               function t() {
                  var e, n, o;
                  !(function (e, t) {
                     if (!(e instanceof t)) throw new TypeError('Cannot call a class as a function');
                  })(this, t);
                  for (var r = arguments.length, i = new Array(r), a = 0; a < r; a++) i[a] = arguments[a];
                  return ne(
                     o,
                     ((n = o = ne(this, (e = oe(t)).call.apply(e, [this].concat(i)))),
                     (o.open = !1),
                     (o.close = function () {
                        o.props.onClose();
                     }),
                     n)
                  );
               }
               var n, o, i;
               return (
                  (n = t),
                  (o = [
                     {
                        key: 'render',
                        value: function () {
                           return r.a.createElement(
                              'div',
                              null,
                              r.a.createElement(
                                 Y.a,
                                 { dimmer: !0, open: this.props.state.open, onClose: this.close, closeIcon: !0 },
                                 r.a.createElement(
                                    Y.a.Header,
                                    { className: 'modalHeader' },
                                    r.a.createElement('span', null, this.props.state.title)
                                 ),
                                 r.a.createElement(
                                    Y.a.Content,
                                    null,
                                    r.a.createElement(
                                       Y.a.Description,
                                       null,
                                       r.a.createElement(
                                          'pre',
                                          { className: 'modal-trim' },
                                          JSON.stringify(this.props.state.content, null, 2)
                                       )
                                    )
                                 )
                              )
                           );
                        }
                     }
                  ]) && te(n.prototype, o),
                  i && te(n, i),
                  (function (e, t) {
                     if ('function' !== typeof t && null !== t)
                        throw new TypeError('Super expression must either be null or a function');
                     ee(e.prototype, t && t.prototype), t && ee(e, t);
                  })(t, e),
                  t
               );
            })(o.Component),
            ie = Object(c.b)(
               function (e) {
                  return { state: e.Modal };
               },
               function (e) {
                  return {
                     onClose: function () {
                        e(j('', '', !1));
                     }
                  };
               }
            )(re);
         n(293);
         function ae(e) {
            return (ae =
               'function' === typeof Symbol && 'symbol' === typeof Symbol.iterator
                  ? function (e) {
                       return typeof e;
                    }
                  : function (e) {
                       return e && 'function' === typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype
                          ? 'symbol'
                          : typeof e;
                    })(e);
         }
         function ce(e, t) {
            return (ce =
               Object.setPrototypeOf ||
               function (e, t) {
                  return (e.__proto__ = t), e;
               })(e, t);
         }
         function le(e, t) {
            for (var n = 0; n < t.length; n++) {
               var o = t[n];
               (o.enumerable = o.enumerable || !1),
                  (o.configurable = !0),
                  'value' in o && (o.writable = !0),
                  Object.defineProperty(e, o.key, o);
            }
         }
         function se(e, t) {
            return !t || ('object' !== ae(t) && 'function' !== typeof t)
               ? (function (e) {
                    if (void 0 === e)
                       throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
                    return e;
                 })(e)
               : t;
         }
         function ue(e) {
            return (ue =
               Object.getPrototypeOf ||
               function (e) {
                  return e.__proto__;
               })(e);
         }
         var fe = (function (e) {
               function t() {
                  return (
                     (function (e, t) {
                        if (!(e instanceof t)) throw new TypeError('Cannot call a class as a function');
                     })(this, t),
                     se(this, ue(t).apply(this, arguments))
                  );
               }
               var n, o, i;
               return (
                  (n = t),
                  (o = [
                     {
                        key: 'render',
                        value: function () {
                           var e = this;
                           return r.a.createElement(
                              u.a,
                              { fluid: !0, className: 'timeline' },
                              r.a.createElement('div', { id: 'dash' }, r.a.createElement(C, { name: 'Dashboard' })),
                              r.a.createElement(
                                 'div',
                                 { id: 'blockDisplay', className: 'blockDisplay' },
                                 r.a.createElement(
                                    g.a,
                                    { className: 'letOverflow' },
                                    this.props.state.map(function (t) {
                                       return r.a.createElement(q, {
                                          key: t,
                                          block: t,
                                          prevBlock: e.props.state[e.getPrevBlock(t)]
                                       });
                                    })
                                 )
                              ),
                              r.a.createElement(ie, null)
                           );
                        }
                     },
                     {
                        key: 'getPrevBlock',
                        value: function (e) {
                           var t = this.props.state.indexOf(e) + 1;
                           return t === this.props.state.length ? -1 : t;
                        }
                     }
                  ]) && le(n.prototype, o),
                  i && le(n, i),
                  (function (e, t) {
                     if ('function' !== typeof t && null !== t)
                        throw new TypeError('Super expression must either be null or a function');
                     ce(e.prototype, t && t.prototype), t && ce(e, t);
                  })(t, e),
                  t
               );
            })(o.Component),
            pe = Object(c.b)(function (e) {
               return { state: e.Blocks };
            })(fe);
         n(291);
         function he(e) {
            return (he =
               'function' === typeof Symbol && 'symbol' === typeof Symbol.iterator
                  ? function (e) {
                       return typeof e;
                    }
                  : function (e) {
                       return e && 'function' === typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype
                          ? 'symbol'
                          : typeof e;
                    })(e);
         }
         function me(e, t) {
            return (me =
               Object.setPrototypeOf ||
               function (e, t) {
                  return (e.__proto__ = t), e;
               })(e, t);
         }
         function ye(e, t) {
            for (var n = 0; n < t.length; n++) {
               var o = t[n];
               (o.enumerable = o.enumerable || !1),
                  (o.configurable = !0),
                  'value' in o && (o.writable = !0),
                  Object.defineProperty(e, o.key, o);
            }
         }
         function de(e, t) {
            return !t || ('object' !== he(t) && 'function' !== typeof t)
               ? (function (e) {
                    if (void 0 === e)
                       throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
                    return e;
                 })(e)
               : t;
         }
         function be(e) {
            return (be =
               Object.getPrototypeOf ||
               function (e) {
                  return e.__proto__;
               })(e);
         }
         var ve = (function (e) {
            function t() {
               return (
                  (function (e, t) {
                     if (!(e instanceof t)) throw new TypeError('Cannot call a class as a function');
                  })(this, t),
                  de(this, be(t).apply(this, arguments))
               );
            }
            var n, o, i;
            return (
               (n = t),
               (o = [
                  {
                     key: 'render',
                     value: function () {
                        return r.a.createElement(
                           'div',
                           { className: 'footer__copyright appfooter' },
                           r.a.createElement(
                              'div',
                              null,
                              r.a.createElement(
                                 'a',
                                 {
                                    className: 'menu__link',
                                    rel: 'noopener noreferrer',
                                    target: '_blank',
                                    href: 'https://www.bigchaindb.com/'
                                 },
                                 '\xa9 2018 BigchainDB GmbH'
                              ),
                              r.a.createElement(
                                 'a',
                                 {
                                    className: 'menu__link',
                                    rel: 'noopener noreferrer',
                                    target: '_blank',
                                    href: 'https://www.bigchaindb.com/terms/'
                                 },
                                 'Terms'
                              ),
                              r.a.createElement(
                                 'a',
                                 {
                                    className: 'menu__link',
                                    rel: 'noopener noreferrer',
                                    target: '_blank',
                                    href: 'https://www.bigchaindb.com/privacy/'
                                 },
                                 'Privacy'
                              )
                           )
                        );
                     }
                  }
               ]) && ye(n.prototype, o),
               i && ye(n, i),
               (function (e, t) {
                  if ('function' !== typeof t && null !== t)
                     throw new TypeError('Super expression must either be null or a function');
                  me(e.prototype, t && t.prototype), t && me(e, t);
               })(t, e),
               t
            );
         })(o.Component);
         n(289);
         function ge(e) {
            return (ge =
               'function' === typeof Symbol && 'symbol' === typeof Symbol.iterator
                  ? function (e) {
                       return typeof e;
                    }
                  : function (e) {
                       return e && 'function' === typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype
                          ? 'symbol'
                          : typeof e;
                    })(e);
         }
         function we(e, t) {
            return (we =
               Object.setPrototypeOf ||
               function (e, t) {
                  return (e.__proto__ = t), e;
               })(e, t);
         }
         function Ee(e, t) {
            for (var n = 0; n < t.length; n++) {
               var o = t[n];
               (o.enumerable = o.enumerable || !1),
                  (o.configurable = !0),
                  'value' in o && (o.writable = !0),
                  Object.defineProperty(e, o.key, o);
            }
         }
         function ke(e, t) {
            return !t || ('object' !== ge(t) && 'function' !== typeof t)
               ? (function (e) {
                    if (void 0 === e)
                       throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
                    return e;
                 })(e)
               : t;
         }
         function _e(e) {
            return (_e =
               Object.getPrototypeOf ||
               function (e) {
                  return e.__proto__;
               })(e);
         }
         var Se = (function (e) {
               function t() {
                  return (
                     (function (e, t) {
                        if (!(e instanceof t)) throw new TypeError('Cannot call a class as a function');
                     })(this, t),
                     ke(this, _e(t).apply(this, arguments))
                  );
               }
               var n, o, i;
               return (
                  (n = t),
                  (o = [
                     {
                        key: 'render',
                        value: function () {
                           return r.a.createElement(
                              u.a,
                              { fluid: !0, className: 'App' },
                              r.a.createElement(v, null),
                              r.a.createElement(u.a, { fluid: !0 }, r.a.createElement(pe, null)),
                              r.a.createElement(ve, null)
                           );
                        }
                     }
                  ]) && Ee(n.prototype, o),
                  i && Ee(n, i),
                  (function (e, t) {
                     if ('function' !== typeof t && null !== t)
                        throw new TypeError('Super expression must either be null or a function');
                     we(e.prototype, t && t.prototype), t && we(e, t);
                  })(t, e),
                  t
               );
            })(o.Component),
            xe = Boolean(
               'localhost' === window.location.hostname ||
                  '[::1]' === window.location.hostname ||
                  window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/)
            );
         function Oe(e) {
            navigator.serviceWorker
               .register(e)
               .then(function (e) {
                  e.onupdatefound = function () {
                     var t = e.installing;
                     t.onstatechange = function () {
                        'installed' === t.state &&
                           (navigator.serviceWorker.controller
                              ? console.log('New content is available; please refresh.')
                              : console.log('Content is cached for offline use.'));
                     };
                  };
               })
               .catch(function (e) {
                  console.error('Error during service worker registration:', e);
               });
         }
         var Te = n(253),
            Ce = {},
            je = function () {
               var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : Ce,
                  t = arguments.length > 1 ? arguments[1] : void 0;
               switch (t.type) {
                  case 'VALID_TX_RECEIVED':
                     return (
                        e.hasOwnProperty(t.blockId)
                           ? (e[t.blockId][t.txId] = t.raw)
                           : ((e[t.blockId] = {}), (e[t.blockId][t.txId] = t.raw)),
                        Object.assign({}, e, e)
                     );
                  default:
                     return e;
               }
            },
            Ne = { title: '', content: null },
            Be = function () {
               var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : Ne,
                  t = arguments.length > 1 ? arguments[1] : void 0;
               switch (t.type) {
                  case 'SET_MODAL':
                     return Object.assign({}, { content: t.content, title: t.title, open: t.open });
                  default:
                     return e;
               }
            },
            Pe = { connected: 'Disconnected', lastBlock: 0, totalTx: 0 },
            He = function () {
               var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : Pe,
                  t = arguments.length > 1 ? arguments[1] : void 0;
               switch (t.type) {
                  case 'UPDATE_STATS':
                     var n = t.connected ? 'Connected to: ' + P.host : 'Disconnected';
                     return Object.assign({}, { connected: n, lastBlock: t.blockHeight, totalTx: t.totalTx });
                  default:
                     return e;
               }
            },
            Ie = [],
            De = function () {
               var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : Ie,
                  t = arguments.length > 1 ? arguments[1] : void 0;
               switch (t.type) {
                  case 'CHECK_BLOCKS':
                     return (
                        e.includes(t.blockId) || e.unshift(t.blockId),
                        e.length > T.maxBlocks && e.splice(T.maxBlocks, e.length - T.maxBlocks),
                        e.slice()
                     );
                  default:
                     return e;
               }
            },
            We = Object(l.combineReducers)({ Transaction: je, Modal: Be, Stats: He, Blocks: De }),
            Re = !1,
            Ae = P.secure ? 'wss://' : 'ws://',
            Le = function (e) {
               var t = new WebSocket(Ae + P.host.split(':')[0] + ':' + P.ws_port + P.api + P.validTx);
               return (
                  (t.onopen = function () {
                     e(N((Re = !0), '---'));
                  }),
                  (t.onmessage = function (t) {
                     var n,
                        o = JSON.parse(t.data);
                     ((n = o.transaction_id),
                     I.getTransaction(n).then(function (e) {
                        return e;
                     })).then(function (t) {
                        var n, r;
                        e(
                           ((n = o.transaction_id),
                           (r = o.height),
                           { type: 'VALID_TX_RECEIVED', txId: n, blockId: r, raw: t })
                        ),
                           e(
                              (function (e) {
                                 return { type: 'CHECK_BLOCKS', blockId: e };
                              })(o.height)
                           ),
                           e(N(Re, o.height));
                     });
                  }),
                  (t.onclose = function () {
                     Re = !1;
                  }),
                  t
               );
            },
            Me = Object(l.createStore)(We, Object(Te.composeWithDevTools)(Object(l.applyMiddleware)(s.a)));
         Le(Me.dispatch),
            a.a.render(
               r.a.createElement(c.a, { store: Me }, r.a.createElement(Se, null)),
               document.getElementById('root')
            ),
            (function () {
               if ('serviceWorker' in navigator) {
                  if (new URL('', window.location).origin !== window.location.origin) return;
                  window.addEventListener('load', function () {
                     var e = ''.concat('', '/service-worker.js');
                     xe
                        ? ((function (e) {
                             fetch(e)
                                .then(function (t) {
                                   404 === t.status || -1 === t.headers.get('content-type').indexOf('javascript')
                                      ? navigator.serviceWorker.ready.then(function (e) {
                                           e.unregister().then(function () {
                                              window.location.reload();
                                           });
                                        })
                                      : Oe(e);
                                })
                                .catch(function () {
                                   console.log('No internet connection found. App is running in offline mode.');
                                });
                          })(e),
                          navigator.serviceWorker.ready.then(function () {
                             console.log(
                                'This web app is being served cache-first by a service worker. To learn more, visit https://goo.gl/SC7cgQ'
                             );
                          }))
                        : Oe(e);
                  });
               }
            })();
      },
      289: function (e, t, n) {},
      291: function (e, t, n) {},
      293: function (e, t, n) {},
      302: function (e, t, n) {},
      304: function (e, t, n) {},
      306: function (e, t, n) {},
      318: function (e, t, n) {},
      48: function (e) {
         e.exports = {
            'create.description': 'asset.data',
            'transfer.description': 'metadata',
            maxBlocks: 100,
            contextName: 'BigchainDB Testnet'
         };
      },
      533: function (e, t, n) {},
      535: function (e, t, n) {},
      555: function (e, t, n) {
         n(554), (e.exports = n(287));
      }
   },
   [[555, 0, 1]]
]);
//# sourceMappingURL=main.1153e0ee.chunk.js.map
