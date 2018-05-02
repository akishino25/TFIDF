<!DOCTYPE html>
<html>

<head>
    <title>選択画面</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="./css/bootstrap.min.css">
    <link rel="stylesheet" href="./css/style.css">
</head> 

<body>
    <div class="container">
        <h2>好きなものをチェックしてください</h2>
        <form action="./checked" method="POST">
            <table class="table table-borderd">
                <tr class="info">
                    <td class="col-md-2">link</td>
                    <td class="col-md-2">title</td>
                    <td class="col-md-7">comment</td>
                    <td class="col-md-1">like</td>
                </tr>
                {% for tb in tables %}
                <tr>
                    <td>{{tb['link']}}</td>
                    <td>{{tb['title']}}</td>
                    <td>{{tb['comment']}}</td>
                    <td>

                        <input type="checkbox" name="likeFlag" value={{tb['link']}}
                        {% if tb['likeflag']==true: %}
                        checked
                        {% endif %}
                        >
                    </td>
                </tr>
                {% endfor %}
            </table>
        <input type="submit" value="送信">
        </form>
    </div>
</body>