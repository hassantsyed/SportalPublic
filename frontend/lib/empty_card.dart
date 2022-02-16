import 'package:flutter/material.dart';

class EmptyCard extends StatelessWidget {
  EmptyCard({@required this.emptyText});

  final emptyText;

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 150,
      child: Center(
        child: Card(
          margin: EdgeInsets.all(10),
          child: Padding(
            padding: const EdgeInsets.only(bottom: 10),
            child: Column(
              children: <Widget>[
                Center(
                  child: ListTile(
                    title: Text(
                      "$emptyText",
                      textAlign: TextAlign.center
                    )
                  )
                ),
              ],
            ),
          ),
        ),
      )
    );
  }
}