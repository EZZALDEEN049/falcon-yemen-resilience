import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent / "code"))
import historical_bgp_replay_v2 as m
import validate_native_ioda
import download_ioda_raw

class Guardrails(unittest.TestCase):
    def row(self,typ,ts,peer_ip='192.0.2.1',prefix='203.0.113.0/24',origin='30873',path='64500 15412 30873'):
        return m.parse_line('|'.join(('R' if typ=='R' else 'U',typ,str(ts),'ris','rrc00','','','64500',peer_ip,prefix,'',path,origin,'','','')))
    def test_withdrawals_are_applied_despite_missing_origin(self):
        rib=[self.row('R',0)]
        updates=[self.row('A',5),self.row('W',10,origin='',path='')]
        a,b,n=m.states_at(rib,updates,{'203.0.113.0/24'},30873,6,12)
        self.assertEqual(len(a),1);self.assertEqual(len(b),0);self.assertEqual(n['withdrawal'],1)
    def test_distinct_peer_ips(self):
        r1=self.row('R',0,'192.0.2.1');r2=self.row('R',0,'192.0.2.2')
        self.assertNotEqual(r1['vantage'],r2['vantage'])
    def test_origin_change_invalidates(self):
        rib=[self.row('R',0)];updates=[self.row('A',5),self.row('A',10,origin='12486',path='64500 12486')]
        a,b,n=m.states_at(rib,updates,{'203.0.113.0/24'},30873,6,12)
        self.assertEqual(len(a),1);self.assertEqual(len(b),0);self.assertEqual(n['origin_change'],1)
    def test_unmatched_vantage_rejected(self):
        r=self.row('R',0)
        with self.assertRaisesRegex(ValueError,'Peer liveness cannot be inferred'):
            m.comparable({(r['vantage'],r['prefix']):r},{})
    def test_ioda_compact_source_series_is_expanded(self):
        payload={'data':[{'datasource':'bgp','from':1578441600,'step':300,'values':[100,95]},{'datasource':'ping-slash24','from':1578441600,'step':300,'values':[80,40]}]}
        rows=download_ioda_raw.flatten_series(payload)
        self.assertEqual(len(rows),4)
        self.assertEqual({r['signal'] for r in rows},{'bgp','ping-slash24'})
        self.assertEqual(sorted({r['timestamp'] for r in rows}),[1578441600,1578441900])
    def test_unknown_native_signal_is_not_accepted_as_bgp(self):
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w+',suffix='.csv') as f:
            f.write('signal,timestamp,value\nunknown,1578441600,10\n')
            f.flush()
            with self.assertRaisesRegex(ValueError,'Multiple or zero raw datasource names'):
                validate_native_ioda.analyze(f.name)
    def test_native_empty_rejected(self):
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w+',suffix='.csv') as f:
            f.write('signal,timestamp,value\n');f.flush()
            with self.assertRaisesRegex(ValueError,'No native IODA rows'):
                validate_native_ioda.analyze(f.name)
if __name__=='__main__':unittest.main(verbosity=2)
