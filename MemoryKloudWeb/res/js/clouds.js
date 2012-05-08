var cloudMoved = false;
var cloud2Moved = false;
var cloud3Moved = false;

$(init);

function init()
{
	cloudMove();
	cloud2Move();
	cloud3Move();
}

function cloudMove()
{
	if (!cloudMoved)
	{
		$("#cloud")
			.css("left", $("#cloud").offset().left)
	}

	$("#cloud")
		.animate(
			{
				left: $("#sky").width()
			},
			cloudMoved ? 180000 : 150000,
			"linear",
			function()
			{
				$(this)
					.css("left", -parseInt($(this).css("width")))
				cloudMoved = true;
				cloudMove();
			}
		)
}

function cloud2Move()
{
	if (!cloud2Moved)
	{
		$("#cloud2")
			.css("left", $("#cloud2").offset().left)
	}
	$("#cloud2")
		.animate(
			{
				left: $("#sky").width()
			},
			cloud2Moved ? 120000 : 60000,
			"linear",
			function()
			{
				$(this)
					.css("left", -parseInt($(this).css("width")))
				cloud2Moved = true;
				cloud2Move();
			}
		)
}

function cloud3Move()
{
	if (!cloud3Moved)
	{
		$("#cloud3")
			.css("left", $("#cloud3").offset().left)
	}
	$("#cloud3")
		.animate(
			{
				left: $("#sky").width()
			},
			cloud3Moved ? 400000 : 150000,
			"linear",
			function()
			{
				$(this)
					.css("left", -parseInt($(this).css("width")))
				cloud3Moved = true;
				cloud3Move();
			}
		)
}
