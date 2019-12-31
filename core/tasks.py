from genetherapy import job


@job.task(bind=True)
def perform_indexing(self,component):
    from core.indexing import ElasticSearchHelper
    try:
        helper = ElasticSearchHelper()
        helper.index(component)
    except Exception as e:
        print (e.message or str(e))