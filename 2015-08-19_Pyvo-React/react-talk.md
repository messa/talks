
React
=====

Petr Messner - <petr.messner@gmail.com>

Problémy s řešením webové aplikace pomocí jQuery:

- callback hell
- problematické generování HTML

[React](http://facebook.github.io/react/) řeší:

- HTML šablonování v Javascriptu

  ```js
  let items = [];
  items.push(<li>first</li>);
  items.push(<li>second</li>);
  return (<ol>{items}</ol>);
  ```

  Do klasického Javascriptu to přeloží [Babel](babeljs.io).

- aktualizace dat na stránce (virtual DOM)


Příklad 1: https://jsfiddle.net/L1qrjL4m/2/

```html
<div id='content'>react DOM will be rendered here</div>
<script src='https://cdnjs.cloudflare.com/ajax/libs/react/0.13.3/react.min.js'></script>
<script type='text/babel'>
    const html = (<div>
        <h1>Hello World!</h1>
    </div>);
    React.render(html, document.getElementById('content'));
</script>
```


Příklad 2: https://jsfiddle.net/L1qrjL4m/3/


Flux
----

https://facebook.github.io/flux/docs/overview.html


Este
----

https://github.com/este/este

[Demo](http://este-demo.messa.cz:8000) - ukázat hot loading, NPM, Gulp a tak

Development vs. production


Python
------

- Flask vs. Node

- services, REST, RPC, [zerorpc](http://www.zerorpc.io/)

Možnosti, jak nasadit React s Pythonem:

- backend celý v Pythonu, vydává "prázdnou stránku", kde se na klientu spustí React
    - protože v Pythonu nemůžeme zavolat `React.renderToString()`
    - nevýhoda: prázdná stránka není ideální pro SEO apod.
- web server v Node (vyrenderuje stránku), Python jako druhý web server poskytující API
    - frontend komunikuje s oběma servery
- web server v Node, která komunikuje s RPC service v Pythonu



Odkazy
------

- http://facebook.github.io/react/
- https://babeljs.io/repl/
- http://www.dzejes.cz/
