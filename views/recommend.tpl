<!DOCTYPE html>
<html>

<head>
    <title>ランキング画面</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="./css/bootstrap.min.css">
    <link rel="stylesheet" href="./css/style.css">
</head> 

<body>
    <div class="container">
        <h2>おすすめランキング</h2>
        <table class="table table-borderd">
            <tr class="info">
                <td class="col-md-1">no</td>
                <td class="col-md-1">score</td>
                <td class="col-md-2">link</td>
                <td class="col-md-2">title</td>
                <td class="col-md-6">comment</td>
            </tr>
            {% for tb in ranking %}
            <tr>
                <td>{{tb['no']}}</td>
                <td>{{tb['score']}}</td>
                <td>{{tb['link']}}</td>
                <td>{{tb['title']}}</td>
                <td>{{tb['comment']}}</td>
            </tr>
            {% endfor %}
        </table>
    </div>
</body>