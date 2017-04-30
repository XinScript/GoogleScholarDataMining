let venues = [
	'GEOCHIMICA ET COSMOCHIMICA S(4) ACTA 66 (15 A), A401-A401, 2002',
	'Quaternary Science Reviews 30 (21), 3152-3170, 2011',
	'NCR-days 2005, 2006',
	'IV hahayolo IV',
	'Geografiska Annaler: Series A, Physical Geography 92 (1), 125-139, 2010',
	'European Geosciences Union General Assembly, EGU2016-938, 2016',
	'Geophysical Research Abstracts v13, EGU General Assembly, 2011',
	'Geophysical Research Abstracts. EGU General Assembly, 10446-10446, 2010',
	'deltares reports',
	'Deltares Reports, 2016',
	'ringing & migration and fuck',
	'asdóasdasd January Sept september',
	'the european biomass conference',
	'The Indian Labour Market and Economic Structural Change, 7, 1994'
]
for (let i in venues) {
	// venue = venue.replace(/e?\d+(th|st|rd|nd)?|\b\w+[-‐–—]\w+\b|\(.+\)|\.{2,}|\b[IVX]+\b/ig, '').replace(/[-‐–—,(;./)'’]+|\s+/g, ' ').trim();
	let venue = venues[i]
		.replace(/\b\w*(\d+)?[-‐–—]\w*\d+\b|\b\w+\d+\b|e?\d+(th|st|rd|nd)?|S?\(.+\)|\[.+\]|\.{2,}|\b[IVX]+\b|[,.]+|\s+&\s+|\b(and|the|of|in|or|for|at|on)\b/ig, '')
		// .replace(/\..+/ig,'')
		.replace(/[-‐–—(;/)'’:]+/g, ' ')
		.replace(/\b(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|June?|July?|Aug(ust)?|Sept(ember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)\b/ig, '')
		.replace(/\s+/g, ' ')
		.trim();

	console.log(venue);
}
// S?\(?
// venue = venue.replace(/S?\(?e?\d+(th|st|rd|nd)?(\-\d+)?\)?|\([\w\d]+[-–\s]?[\w\d]+\)|\.{2,}|\s+[IVX]+$|^[IVX]+\s+|\s+[IVX]+\s+/ig, '').replace(/[-‐–—,(;./)'’]+|\s+/g,' ').trim();