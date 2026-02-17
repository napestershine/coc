/// Data model for Clash of Clans player account
class COCAccount {
  final String tag;
  final String name;
  final int townHallLevel;
  final int expLevel;
  final int trophies;
  final int bestTrophies;
  final int donations;
  final int donationsReceived;
  final int attackWins;
  final int defenseWins;
  final String clanTag;
  final String role;
  final List<dynamic>? troopsUnlocked;
  final List<dynamic>? spellsUnlocked;
  final List<dynamic>? buildingsUnderConstruction;
  final List<dynamic>? researchUnderConstruction;
  final List<dynamic>? petsUnderConstruction;

  COCAccount({
    required this.tag,
    required this.name,
    required this.townHallLevel,
    required this.expLevel,
    required this.trophies,
    required this.bestTrophies,
    required this.donations,
    required this.donationsReceived,
    required this.attackWins,
    required this.defenseWins,
    required this.clanTag,
    required this.role,
    this.troopsUnlocked,
    this.spellsUnlocked,
    this.buildingsUnderConstruction,
    this.researchUnderConstruction,
    this.petsUnderConstruction,
  });

  /// Factory constructor to parse JSON response from Clash of Clans API
  factory COCAccount.fromJson(Map<String, dynamic> json) {
    return COCAccount(
      tag: json['tag'] ?? '',
      name: json['name'] ?? 'Unknown',
      townHallLevel: json['townHallLevel'] ?? 0,
      expLevel: json['expLevel'] ?? 0,
      trophies: json['trophies'] ?? 0,
      bestTrophies: json['bestTrophies'] ?? 0,
      donations: json['donations'] ?? 0,
      donationsReceived: json['donationsReceived'] ?? 0,
      attackWins: json['attackWins'] ?? 0,
      defenseWins: json['defenseWins'] ?? 0,
      clanTag: json['clan']?['tag'] ?? 'N/A',
      role: json['role'] ?? 'member',
      troopsUnlocked: json['troops'],
      spellsUnlocked: json['spells'],
      buildingsUnderConstruction: json['buildingsUnderConstruction'],
      researchUnderConstruction: json['researchUnderConstruction'],
      petsUnderConstruction: json['petsUnderConstruction'],
    );
  }

  @override
  String toString() => 'COCAccount(tag: $tag, name: $name, townHallLevel: $townHallLevel)';
}
