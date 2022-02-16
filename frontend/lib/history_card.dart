import 'package:flutter/material.dart';
import 'package:material_design_icons_flutter/material_design_icons_flutter.dart';
import 'match.dart';

class HistoryCard extends StatelessWidget {
  HistoryCard({@required this.match});

  final Match match;

  @override
  Widget build(BuildContext context) {
    MaterialColor cardColor = Colors.grey;
    String winner;
    TextSpan team1 = TextSpan(text: match.team1.name);
    TextSpan team2 = TextSpan(text: match.team2.name);
    if (match.status == "TIE") {
      winner = "Tie";
    } else {
      if (match.status == "TEAM1") {
        winner = match.team1.name;
      } else {
        winner = match.team2.name;
      }
    }
    if (match.pick != null) {
      if (match.status == "TIE") {
        cardColor = Colors.indigo;
      } else if (match.pick == match.status) {
        cardColor = Colors.green;
      } else {
        cardColor = Colors.red;
      }
      if (match.pick == "TEAM1") {
        team1 = TextSpan(text: match.team1.name, style: TextStyle(color: Colors.blue));
      } else if (match.pick == "TEAM2") {
        team2 = TextSpan(text: match.team2.name, style: TextStyle(color: Colors.blue));
      }
    }

    Row winnerRow = Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(winner, style: TextStyle(fontSize: 18)),
      ],
    );
    if (match.result.isNotEmpty) {
      winnerRow.children.add(Text(match.result, style: TextStyle(fontSize: 12)));
    }
    return Card(
      elevation: 5,
      child: Padding(
        padding: const EdgeInsets.all(2),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: <Widget>[
            ListTile(
              leading: Icon(MdiIcons.circle, color: cardColor,),
              title: winnerRow,
              subtitle: RichText(
                  text: TextSpan(
                    style: TextStyle(color: Colors.black),
                    children: [
                      team1,
                      TextSpan(text: " V. "),
                      team2
                    ]
                  ),
                ),
            ),
          ],
        ) 
      ),
    );
  }
}