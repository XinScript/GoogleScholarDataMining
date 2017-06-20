import DB as db
from Chart import Chart

copy = db.get_researcher_copy()
chart_path = '../charts/discipline '

# chart = Chart(6,5)

# # chart.pie([16820,8910],'percentage of researcher with a portrait',['with portrait','without portrait'])
# # chart.save('portrait_percentage.eps')
# # chart.clear()

# chart.pie([12970,2674],'gender vs female',['male','female'])
# chart.save('gender ratio.eps')



# # db.getCollection('researcher__copies').aggregate([{'$project':{'_id':1,'count':{'$size':'$pubs'}}},{'$group':{'_id':'','total':{'$sum':'$count'}}}])



average_h_index(30)