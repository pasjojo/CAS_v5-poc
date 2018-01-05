<!DOCTYPE html>
<html lang="en">
<head>
<title>Apache client PoC !</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
</head>
<body>
<div class="container">
<h1>Contenu sécurisé</h1>
<img src="logo_CA_France_RVB.png" border="0"/ class="img-responsive img-rounded" alt="Logo APCA" />
<p>&nbsp;</p>
<p><big>Visible uniquement après la saisie des identifiants de connexion</big></p>
<h2>Attributs retournés par CAS</h2>
<?php
echo "<pre>";
if (array_key_exists('REMOTE_USER', $_SERVER)) {
  echo "REMOTE_USER = " . $_SERVER['REMOTE_USER'] . "<br>";
}
$headers = getallheaders();
foreach ($headers as $key => $value) {
  if (strpos($key, 'CAS_') === 0) {
    echo substr($key, 4) . " = " . $value . "<br>";
  }
}
echo "</pre>";
?>
</div>
</body>
</html>
