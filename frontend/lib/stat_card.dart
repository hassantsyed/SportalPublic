import 'package:flutter/material.dart';
import 'GroupPick.dart';
import 'package:charts_flutter/flutter.dart' as charts;

class StatCard extends StatelessWidget {
  StatCard({@required this.groupPick, Key key}) : super(key: key);

  final GroupPick groupPick;

  @override
  Widget build(BuildContext context) {
    charts.Color player1 = charts.ColorUtil.fromDartColor(Colors.indigoAccent);
    charts.Color player2 = charts.ColorUtil.fromDartColor(Colors.indigoAccent);
    if (groupPick.winner == "TEAM1") {
      player1 = charts.ColorUtil.fromDartColor(Colors.green);
      player2 = charts.ColorUtil.fromDartColor(Colors.red);
    } else if (groupPick.winner == "TEAM2") {
      player1 = charts.ColorUtil.fromDartColor(Colors.red);
      player2 = charts.ColorUtil.fromDartColor(Colors.green);
    }
    List<charts.Series<OrdinalData, String>> series = [
      charts.Series(
        id: groupPick.mid.toString(),
        data: [OrdinalData(groupPick.player1, groupPick.team1Count, player1), OrdinalData(groupPick.player2, groupPick.team2Count, player2)],
        domainFn: (OrdinalData series, _) => series.name,
        measureFn: (OrdinalData series, _) => series.count,
        colorFn: (OrdinalData series, _) => series.color
      )
    ];

    return Card(
      child: Container(
        height: 200,
        child: charts.BarChart(
          series, 
          animate: true,
          vertical: false,
          barRendererDecorator: charts.BarLabelDecorator<String>(),
          domainAxis: charts.OrdinalAxisSpec(renderSpec: charts.NoneRenderSpec())
        )
      )
    );
  }
}

class OrdinalData {
  final String name;
  final int count;
  final charts.Color color;

  OrdinalData(this.name, this.count, this.color);
}