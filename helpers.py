import yql


def do_yql(query):
	y = yql.Public()
	result = y.execute(query)
	return result


def get_nearest_centres(postcode):
	query = "select * from html where url=\"http://www.ukonlinecentres.com/centresearch/index.php?q=%s\" and xpath=\"//div[@class=\'center_details\']\"" % postcode
	try:
		results = do_yql(query)['query']['results']['div']
		records = []
		if results:
			for result in results:
				# initialise some properties we may never be lucky enough to see to False...
				distance = False
				fax = False
				email = False
				website = False
				firsturl = False
				secondurl = False
				# pull apart the JSON from YQL 
				info = result
				title = info['h4'].strip()
				address = info['div'][0]['p'].replace(", ,", ",").strip()
				phone = info['div'][1]['p'].replace("Tel.", "").strip()
				if "fax" in info['div'][2]['p'].lower():
					fax = info['div'][2]['p'].replace("Fax.", "").strip()
				else:
					distance = info['div'][2]['p'].replace("distance ", "").strip()
				if "distance" in str(info['div'][3]).lower():
					distance = (info['div'][3]['p'].replace("distance ", "").strip())
				else:
					firsturl = info['div'][3]['a']['href']
				try:
					if "href" in str(info['div'][4]).lower():
						href = info['div'][4]['a']['href']
						if firsturl:
							secondurl = href
						else:
							firsturl = href
				except:
					errors = True
				try:
					if "href" in str(info['div'][5]).lower():
						secondurl = info['div'][5]['a']['href']
				except:
					errors = True
				email = firsturl.replace("mailto:", "")
				if len(email) < 5:
					email = False
				website = secondurl
				if website:
					if len(website) <= 7:
						website = False
				record = {
					"title": title,
					"address": address,
					"phone": phone,
					"fax": fax,
					"distance": distance,
					"email": email,
					"website": website
				}
				records.append(record)
	except:
		records = False
	return records, query