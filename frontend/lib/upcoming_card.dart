import 'package:flutter/material.dart';
import 'package:flutter/cupertino.dart';
import 'package:provider/provider.dart';
import 'match_service.dart';
import 'match.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';

class UpcomingCard extends StatelessWidget {
  UpcomingCard({@required this.match, Key key}) : super(key: key);

  final Match match;

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 5,
      child: Padding(
        padding: const EdgeInsets.only(bottom: 10, top: 10),
        child: Column(
          children: <Widget>[
            Container(
              alignment: Alignment.center,
              child: LayoutBuilder(builder: (context, constraints) {
                return UpcomingButton(match: match, constraints: constraints, key: ValueKey(match.mid));
              })
            ),
          ],
        ),
      ),
    );
  }
}

class UpcomingButton extends StatefulWidget {
  final Match match;
  final BoxConstraints constraints;

  UpcomingButton({@required this.match, @required this.constraints, Key key}) : super(key: key);

  @override
  _UpcomingButtonState createState() => _UpcomingButtonState(match: match, constraints: constraints);
}

class _UpcomingButtonState extends State<UpcomingButton> {
  _UpcomingButtonState({@required this.match, @required this.constraints});
  final Match match;
  final BoxConstraints constraints;

  List<bool> isSelected = [false, false];

  @override
  void initState() {
    super.initState();
    setState(() {
      if (match?.pick == "TEAM1") {
        isSelected[0] = true;
      } else if (match?.pick == "TEAM2") {
        isSelected[1] = true;
      }
    });
  }

  void onPress(int idx) {
    
    setState(() {
      if (isSelected[idx] == true) {
        isSelected[idx] = false;
        match.pick = null;
        Provider.of<MatchService>(context, listen: false).submitPick(match, -1);
      } else {
        isSelected[idx] = true;
        if (idx == 0) {
          match.pick = "TEAM1";
        } else {
          match.pick = "TEAM2";
        }
        Provider.of<MatchService>(context, listen: false).submitPick(match, idx);
      }
      for (int btnIdx = 0; btnIdx < 2; btnIdx++) {
        if (btnIdx != idx) {
          isSelected[btnIdx] = false;
        }
      }
    });
  }

  _buildWidget() {
    if (match.loading) {
      return Center(
        child: LinearProgressIndicator()
      );
    }
    if (match.fail) {
      return Center(
        child: Text("Failure Submitting Pick. Please Retry."),
      );
    }
    if (match.status == "ONGOING") {
      TextSpan team1 = TextSpan(text: match.team1.name);
      TextSpan team2 = TextSpan(text: match.team2.name);
      String selection = "No Selection";
      if (isSelected[0]) {
        selection = match.team1.name;
        team1 = TextSpan(text: match.team1.name, style: TextStyle(color: Colors.blue),);
      } else if (isSelected[1]) {
        selection = match.team2.name;
        team2 = TextSpan(text: match.team2.name, style: TextStyle(color: Colors.blue),);
      } else {
        selection = "No Selection";
      }
      return Column(
        children: [
          RichText(
            text: TextSpan(
              style: TextStyle(color: Colors.black),
              children: [
                team1,
                TextSpan(text: " V. "),
                team2
              ]
            ),
          ),
          Divider(),
          SpinKitPouringHourglass(color: Colors.blue,)
        ],
      );
    }
    return ToggleButtons( 
      constraints: BoxConstraints.expand(width: constraints.maxWidth / 2.5),
      children: <Widget>[
        Text(
          "${match.team1.name}",
          style: TextStyle(
            fontSize: 18
          ),
          textAlign: TextAlign.center,
        ),
        Text(
          "${match.team2.name}",
          style: TextStyle(
            fontSize: 18
          ),
          textAlign: TextAlign.center,
        )
      ],
      onPressed: onPress,
      isSelected: isSelected,
      selectedColor: Colors.blue,
      borderRadius: BorderRadius.circular(10),
      borderColor: Colors.grey,
      selectedBorderColor: Colors.grey,
    );
  }

  @override
  Widget build(BuildContext context) {
    return _buildWidget();
  }
}