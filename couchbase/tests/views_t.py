#  Copyright 2016-2022. Couchbase, Inc.
#  All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License")
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import json
import threading
from datetime import timedelta

import pytest

from couchbase.exceptions import DesignDocumentNotFoundException
from couchbase.management.views import DesignDocumentNamespace
from couchbase.options import ViewOptions
from couchbase.serializer import DefaultJsonSerializer
from couchbase.views import (ViewErrorMode,
                             ViewMetaData,
                             ViewOrdering,
                             ViewQuery,
                             ViewScanConsistency)
from tests.environments import CollectionType
from tests.environments.views_environment import ViewsTestEnvironment


class ViewsParamSuite:
    TEST_MANIFEST = [
        'test_params_base',
        'test_params_client_context_id',
        'test_params_debug',
        'test_params_endkey',
        'test_params_endkey_docid',
        'test_params_group',
        'test_params_group_level',
        'test_params_inclusive_end',
        'test_params_key',
        'test_params_keys',
        'test_params_limit',
        'test_params_namespace',
        'test_params_on_error',
        'test_params_order',
        'test_params_reduce',
        'test_params_scan_consistency',
        'test_params_serializer',
        'test_params_skip',
        'test_params_startkey',
        'test_params_startkey_docid',
        'test_params_timeout',
    ]

    @pytest.fixture(scope='class')
    def base_opts(self, cb_env):
        return {'bucket_name': 'default',
                'document_name': cb_env.DOCNAME,
                'view_name': cb_env.TEST_VIEW_NAME
                }

    def test_params_base(self, cb_env, base_opts):
        opts = ViewOptions()
        query = ViewQuery.create_view_query_object('default', cb_env.DOCNAME, cb_env.TEST_VIEW_NAME, opts)
        params = query.as_encodable()
        assert params == base_opts

    def test_params_client_context_id(self, cb_env, base_opts):
        opts = ViewOptions(client_context_id='test-context-id')
        query = ViewQuery.create_view_query_object('default', cb_env.DOCNAME, cb_env.TEST_VIEW_NAME, opts)

        exp_opts = base_opts.copy()
        exp_opts['client_context_id'] = 'test-context-id'
        params = query.as_encodable()
        assert params == exp_opts

    def test_params_debug(self, cb_env, base_opts):
        opts = ViewOptions(debug=True)
        query = ViewQuery.create_view_query_object('default', cb_env.DOCNAME, cb_env.TEST_VIEW_NAME, opts)

        exp_opts = base_opts.copy()
        exp_opts['debug'] = True
        params = query.as_encodable()
        assert params == exp_opts

    def test_params_endkey(self, cb_env, base_opts):
        key = ['101 Coffee Shop', 'landmark_11769']
        opts = ViewOptions(endkey=key)
        query = ViewQuery.create_view_query_object('default', cb_env.DOCNAME, cb_env.TEST_VIEW_NAME, opts)

        exp_opts = base_opts.copy()
        exp_opts['end_key'] = json.dumps(key)
        params = query.as_encodable()
        assert params == exp_opts

    def test_params_endkey_docid(self, cb_env, base_opts):
        key = 'landmark_11769'
        opts = ViewOptions(endkey_docid=key)
        query = ViewQuery.create_view_query_object('default', cb_env.DOCNAME, cb_env.TEST_VIEW_NAME, opts)

        exp_opts = base_opts.copy()
        exp_opts['end_key_doc_id'] = key
        params = query.as_encodable()
        assert params == exp_opts

    def test_params_group(self, cb_env, base_opts):
        opts = ViewOptions(group=True)
        query = ViewQuery.create_view_query_object('default', cb_env.DOCNAME, cb_env.TEST_VIEW_NAME, opts)

        exp_opts = base_opts.copy()
        exp_opts['group'] = True
        params = query.as_encodable()
        assert params == exp_opts

    def test_params_group_level(self, cb_env, base_opts):
        opts = ViewOptions(group_level=10)
        query = ViewQuery.create_view_query_object('default', cb_env.DOCNAME, cb_env.TEST_VIEW_NAME, opts)

        exp_opts = base_opts.copy()
        exp_opts['group_level'] = 10
        params = query.as_encodable()
        assert params == exp_opts

    def test_params_inclusive_end(self, cb_env, base_opts):
        opts = ViewOptions(inclusive_end=True)
        query = ViewQuery.create_view_query_object('default', cb_env.DOCNAME, cb_env.TEST_VIEW_NAME, opts)

        exp_opts = base_opts.copy()
        exp_opts['inclusive_end'] = True
        params = query.as_encodable()
        assert params == exp_opts

    def test_params_key(self, cb_env, base_opts):
        opts = ViewOptions(key='test-key')
        query = ViewQuery.create_view_query_object('default', cb_env.DOCNAME, cb_env.TEST_VIEW_NAME, opts)

        exp_opts = base_opts.copy()
        exp_opts['key'] = json.dumps('test-key')
        params = query.as_encodable()
        assert params == exp_opts

    def test_params_keys(self, cb_env, base_opts):
        test_keys = ['test-key1', 'test-key2']
        opts = ViewOptions(keys=test_keys)
        query = ViewQuery.create_view_query_object('default', cb_env.DOCNAME, cb_env.TEST_VIEW_NAME, opts)

        exp_opts = base_opts.copy()
        exp_opts['keys'] = list(map(lambda k: json.dumps(k), test_keys))
        params = query.as_encodable()
        assert params == exp_opts

    def test_params_limit(self, cb_env, base_opts):
        opts = ViewOptions(limit=10)
        query = ViewQuery.create_view_query_object('default', cb_env.DOCNAME, cb_env.TEST_VIEW_NAME, opts)

        exp_opts = base_opts.copy()
        exp_opts['limit'] = 10
        params = query.as_encodable()
        assert params == exp_opts

    def test_params_namespace(self, cb_env, base_opts):
        opts = ViewOptions(namespace=DesignDocumentNamespace.DEVELOPMENT)
        query = ViewQuery.create_view_query_object('default', cb_env.DOCNAME, cb_env.TEST_VIEW_NAME, opts)

        exp_opts = base_opts.copy()
        exp_opts['namespace'] = DesignDocumentNamespace.DEVELOPMENT.value
        params = query.as_encodable()
        assert params == exp_opts
        assert query.namespace == DesignDocumentNamespace.DEVELOPMENT

    def test_params_on_error(self, cb_env, base_opts):
        opts = ViewOptions(on_error=ViewErrorMode.CONTINUE)
        query = ViewQuery.create_view_query_object('default', cb_env.DOCNAME, cb_env.TEST_VIEW_NAME, opts)

        exp_opts = base_opts.copy()
        exp_opts['on_error'] = ViewErrorMode.CONTINUE.value
        params = query.as_encodable()
        assert params == exp_opts
        assert query.on_error == ViewErrorMode.CONTINUE

    def test_params_order(self, cb_env, base_opts):
        opts = ViewOptions(order=ViewOrdering.ASCENDING)
        query = ViewQuery.create_view_query_object('default', cb_env.DOCNAME, cb_env.TEST_VIEW_NAME, opts)

        exp_opts = base_opts.copy()
        exp_opts['order'] = ViewOrdering.ASCENDING.value
        params = query.as_encodable()
        assert params == exp_opts
        assert query.order == ViewOrdering.ASCENDING

    def test_params_reduce(self, cb_env, base_opts):
        opts = ViewOptions(reduce=True)
        query = ViewQuery.create_view_query_object('default', cb_env.DOCNAME, cb_env.TEST_VIEW_NAME, opts)

        exp_opts = base_opts.copy()
        exp_opts['reduce'] = True
        params = query.as_encodable()
        assert params == exp_opts

    def test_params_scan_consistency(self, cb_env, base_opts):
        opts = ViewOptions(scan_consistency=ViewScanConsistency.REQUEST_PLUS)
        query = ViewQuery.create_view_query_object('default', cb_env.DOCNAME, cb_env.TEST_VIEW_NAME, opts)

        exp_opts = base_opts.copy()
        exp_opts['scan_consistency'] = ViewScanConsistency.REQUEST_PLUS.value
        params = query.as_encodable()
        assert params == exp_opts
        assert query.consistency == ViewScanConsistency.REQUEST_PLUS

    def test_params_serializer(self, cb_env, base_opts):
        serializer = DefaultJsonSerializer()
        opts = ViewOptions(serializer=serializer)
        query = ViewQuery.create_view_query_object('default', cb_env.DOCNAME, cb_env.TEST_VIEW_NAME, opts)

        exp_opts = base_opts.copy()
        exp_opts['serializer'] = serializer
        params = query.as_encodable()
        assert params == exp_opts

    def test_params_skip(self, cb_env, base_opts):
        opts = ViewOptions(skip=10)
        query = ViewQuery.create_view_query_object('default', cb_env.DOCNAME, cb_env.TEST_VIEW_NAME, opts)

        exp_opts = base_opts.copy()
        exp_opts['skip'] = 10
        params = query.as_encodable()
        assert params == exp_opts

    def test_params_startkey(self, cb_env, base_opts):
        key = ['101 Coffee Shop', 'landmark_11769']
        opts = ViewOptions(startkey=key)
        query = ViewQuery.create_view_query_object('default', cb_env.DOCNAME, cb_env.TEST_VIEW_NAME, opts)

        exp_opts = base_opts.copy()
        exp_opts['start_key'] = json.dumps(key)
        params = query.as_encodable()
        assert params == exp_opts

    def test_params_startkey_docid(self, cb_env, base_opts):
        key = 'landmark_11769'
        opts = ViewOptions(startkey_docid=key)
        query = ViewQuery.create_view_query_object('default', cb_env.DOCNAME, cb_env.TEST_VIEW_NAME, opts)

        exp_opts = base_opts.copy()
        exp_opts['start_key_doc_id'] = key
        params = query.as_encodable()
        assert params == exp_opts

    def test_params_timeout(self, cb_env, base_opts):
        opts = ViewOptions(timeout=timedelta(seconds=20))
        query = ViewQuery.create_view_query_object('default', cb_env.DOCNAME, cb_env.TEST_VIEW_NAME, opts)

        exp_opts = base_opts.copy()
        exp_opts['timeout'] = 20000000
        params = query.as_encodable()
        assert params == exp_opts

        opts = ViewOptions(timeout=20)
        query = ViewQuery.create_view_query_object('default', cb_env.DOCNAME, cb_env.TEST_VIEW_NAME, opts)

        exp_opts = base_opts.copy()
        exp_opts['timeout'] = 20000000
        params = query.as_encodable()
        assert params == exp_opts

        opts = ViewOptions(timeout=25.5)
        query = ViewQuery.create_view_query_object('default', cb_env.DOCNAME, cb_env.TEST_VIEW_NAME, opts)

        exp_opts = base_opts.copy()
        exp_opts['timeout'] = 25500000
        params = query.as_encodable()
        assert params == exp_opts


class ViewsTestSuite:
    TEST_MANIFEST = [
        'test_bad_view_query',
        'test_view_query',
        'test_view_query_ascending',
        'test_view_query_descending',
        'test_view_query_endkey',
        'test_view_query_endkey_docid',
        'test_view_query_in_thread',
        'test_view_query_key',
        'test_view_query_keys',
        'test_view_query_startkey',
        'test_view_query_startkey_docid',
    ]

    def test_bad_view_query(self, cb_env):
        view_result = cb_env.bucket.view_query('fake-ddoc',
                                               'fake-view',
                                               limit=10,
                                               namespace=DesignDocumentNamespace.DEVELOPMENT)

        with pytest.raises(DesignDocumentNotFoundException):
            [r for r in view_result]

    def test_view_query(self, cb_env):

        expected_count = 10
        view_result = cb_env.bucket.view_query(cb_env.DOCNAME,
                                               cb_env.TEST_VIEW_NAME,
                                               limit=expected_count,
                                               namespace=DesignDocumentNamespace.DEVELOPMENT)

        cb_env.assert_rows(view_result, expected_count)

        metadata = view_result.metadata()
        assert isinstance(metadata, ViewMetaData)
        assert metadata.total_rows() >= expected_count

    def test_view_query_ascending(self, cb_env):

        expected_count = 10
        view_result = cb_env.bucket.view_query(cb_env.DOCNAME,
                                               cb_env.TEST_VIEW_NAME,
                                               limit=expected_count,
                                               namespace=DesignDocumentNamespace.DEVELOPMENT,
                                               order=ViewOrdering.ASCENDING)

        rows = cb_env.assert_rows(view_result, expected_count, return_rows=True)
        results = list(map(lambda r: r.key, rows))
        sorted_results = sorted(results, key=lambda x: x[0], reverse=True)
        assert results == sorted_results

        metadata = view_result.metadata()
        assert isinstance(metadata, ViewMetaData)
        assert metadata.total_rows() >= expected_count

    def test_view_query_descending(self, cb_env):
        expected_count = 10
        view_result = cb_env.bucket.view_query(cb_env.DOCNAME,
                                               cb_env.TEST_VIEW_NAME,
                                               limit=expected_count,
                                               namespace=DesignDocumentNamespace.DEVELOPMENT,
                                               order=ViewOrdering.DESCENDING)

        rows = cb_env.assert_rows(view_result, expected_count, return_rows=True)
        results = list(map(lambda r: r.key, rows))
        sorted_results = sorted(results, key=lambda x: x[0])
        assert results == sorted_results

        metadata = view_result.metadata()
        assert isinstance(metadata, ViewMetaData)
        assert metadata.total_rows() >= expected_count

    def test_view_query_endkey(self, cb_env):
        batch_id = cb_env.get_batch_id()
        expected_count = 5
        opts = ViewOptions(limit=expected_count,
                           namespace=DesignDocumentNamespace.DEVELOPMENT,
                           endkey=[f'{batch_id}::10', f'{batch_id}::20'])
        view_result = cb_env.bucket.view_query(cb_env.DOCNAME,
                                               cb_env.TEST_VIEW_NAME,
                                               opts)

        cb_env.assert_rows(view_result, expected_count)

        metadata = view_result.metadata()
        assert isinstance(metadata, ViewMetaData)
        assert metadata.total_rows() >= expected_count

    def test_view_query_endkey_docid(self, cb_env):
        batch_id = cb_env.get_batch_id()
        expected_count = 5
        opts = ViewOptions(limit=expected_count,
                           namespace=DesignDocumentNamespace.DEVELOPMENT,
                           endkey_docid=f'{batch_id}::15')
        view_result = cb_env.bucket.view_query(cb_env.DOCNAME,
                                               cb_env.TEST_VIEW_NAME,
                                               opts)

        cb_env.assert_rows(view_result, expected_count)

        metadata = view_result.metadata()
        assert isinstance(metadata, ViewMetaData)
        assert metadata.total_rows() >= expected_count

    def test_view_query_in_thread(self, cb_env):
        results = [None]

        def run_test(bucket, doc_name, view_name, opts, assert_fn, results):
            try:
                result = bucket.view_query(doc_name, view_name, opts)
                assert_fn(result, opts['limit'])
                assert result.metadata() is not None
            except AssertionError:
                results[0] = False
            except Exception as ex:
                results[0] = ex
            else:
                results[0] = True

        expected_count = 5
        opts = ViewOptions(limit=expected_count,
                           namespace=DesignDocumentNamespace.DEVELOPMENT)
        t = threading.Thread(target=run_test,
                             args=(cb_env.bucket,
                                   cb_env.DOCNAME,
                                   cb_env.TEST_VIEW_NAME,
                                   opts,
                                   cb_env.assert_rows,
                                   results))
        t.start()
        t.join()

        assert len(results) == 1
        assert results[0] is True

    def test_view_query_key(self, cb_env):
        batch_id = cb_env.get_batch_id()
        expected_count = 1
        opts = ViewOptions(limit=expected_count,
                           namespace=DesignDocumentNamespace.DEVELOPMENT,
                           key=[f'{batch_id}', f'{batch_id}::10'])
        view_result = cb_env.bucket.view_query(cb_env.DOCNAME,
                                               cb_env.TEST_VIEW_NAME,
                                               opts)

        cb_env.assert_rows(view_result, expected_count)

        metadata = view_result.metadata()
        assert isinstance(metadata, ViewMetaData)
        assert metadata.total_rows() >= expected_count

    def test_view_query_keys(self, cb_env):
        batch_id = cb_env.get_batch_id()
        expected_count = 5
        keys = [[f'{batch_id}', f'{batch_id}::0'],
                [f'{batch_id}', f'{batch_id}::1'],
                [f'{batch_id}', f'{batch_id}::2'],
                [f'{batch_id}', f'{batch_id}::3'],
                [f'{batch_id}', f'{batch_id}::4']]
        opts = ViewOptions(limit=expected_count,
                           namespace=DesignDocumentNamespace.DEVELOPMENT,
                           keys=keys)
        view_result = cb_env.bucket.view_query(cb_env.DOCNAME,
                                               cb_env.TEST_VIEW_NAME,
                                               opts)

        cb_env.assert_rows(view_result, expected_count)

        metadata = view_result.metadata()
        assert isinstance(metadata, ViewMetaData)
        assert metadata.total_rows() >= expected_count

    def test_view_query_startkey(self, cb_env):
        batch_id = cb_env.get_batch_id()
        expected_count = 5
        opts = ViewOptions(limit=expected_count,
                           namespace=DesignDocumentNamespace.DEVELOPMENT,
                           startkey=[f'{batch_id}', f'{batch_id}::0'])
        view_result = cb_env.bucket.view_query(cb_env.DOCNAME,
                                               cb_env.TEST_VIEW_NAME,
                                               opts)

        cb_env.assert_rows(view_result, expected_count)

        metadata = view_result.metadata()
        assert isinstance(metadata, ViewMetaData)
        assert metadata.total_rows() >= expected_count

    def test_view_query_startkey_docid(self, cb_env):
        batch_id = cb_env.get_batch_id()
        expected_count = 5
        opts = ViewOptions(limit=expected_count,
                           namespace=DesignDocumentNamespace.DEVELOPMENT,
                           startkey_docid=f'{batch_id}::0')
        view_result = cb_env.bucket.view_query(cb_env.DOCNAME,
                                               cb_env.TEST_VIEW_NAME,
                                               opts)

        cb_env.assert_rows(view_result, expected_count)

        metadata = view_result.metadata()
        assert isinstance(metadata, ViewMetaData)
        assert metadata.total_rows() >= expected_count


class ClassicViewsParamTests(ViewsParamSuite):
    @pytest.fixture(scope='class')
    def test_manifest_validated(self):
        def valid_test_method(meth):
            attr = getattr(ClassicViewsParamTests, meth)
            return callable(attr) and not meth.startswith('__') and meth.startswith('test')
        method_list = [meth for meth in dir(ClassicViewsParamTests) if valid_test_method(meth)]
        compare = set(ViewsParamSuite.TEST_MANIFEST).difference(method_list)
        return compare

    @pytest.fixture(scope='class', name='cb_env', params=[CollectionType.DEFAULT])
    def couchbase_test_environment(self, cb_base_env, test_manifest_validated, request):
        if test_manifest_validated:
            pytest.fail(f'Test manifest not validated.  Missing tests: {test_manifest_validated}.')

        cb_env = ViewsTestEnvironment.from_environment(cb_base_env)
        cb_env.enable_views_mgmt()
        cb_env.setup(request.param, test_suite=self.__class__.__name__)
        yield cb_env
        cb_env.teardown(request.param, test_suite=self.__class__.__name__)


class ClassicViewsTests(ViewsTestSuite):
    @pytest.fixture(scope='class')
    def test_manifest_validated(self):
        def valid_test_method(meth):
            attr = getattr(ClassicViewsTests, meth)
            return callable(attr) and not meth.startswith('__') and meth.startswith('test')
        method_list = [meth for meth in dir(ClassicViewsTests) if valid_test_method(meth)]
        compare = set(ViewsTestSuite.TEST_MANIFEST).difference(method_list)
        return compare

    @pytest.fixture(scope='class', name='cb_env', params=[CollectionType.DEFAULT])
    def couchbase_test_environment(self, cb_base_env, test_manifest_validated, request):
        if test_manifest_validated:
            pytest.fail(f'Test manifest not validated.  Missing tests: {test_manifest_validated}.')

        cb_env = ViewsTestEnvironment.from_environment(cb_base_env)
        cb_env.enable_views_mgmt()
        cb_env.setup(request.param)
        yield cb_env
        cb_env.teardown(request.param)
