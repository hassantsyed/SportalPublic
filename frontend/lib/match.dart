import 'team.dart';

class Match {
  final int mid;
  final int lid;
  final Team team1;
  final Team team2;
  final DateTime date;
  final String status;
  String pick;
  bool loading = false;
  bool fail = false;
  String result;

  Match(this.mid, this.lid, this.team1, this.team2, this.status, this.date, this.result);

}