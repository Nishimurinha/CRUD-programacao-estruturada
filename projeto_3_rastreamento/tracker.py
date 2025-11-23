# tracker.py
import math

class EuclideanDistTracker:
    def __init__(self):
        # dicionário: id -> (cx, cy)
        self.center_points = {}
        self.id_count = 0

    def update(self, objects_rect):
        """
        objects_rect: lista de [x, y, w, h] detectados no frame atual.
        Retorna: lista de [x, y, w, h, id].
        """
        objects_bbs_ids = []

        # calcula centros dos novos objetos
        for rect in objects_rect:
            x, y, w, h = rect
            cx = x + w // 2
            cy = y + h // 2

            same_object_detected = False

            for object_id, (px, py) in self.center_points.items():
                dist = math.hypot(cx - px, cy - py)

                # se está perto, considera o mesmo carro
                if dist < 50:
                    self.center_points[object_id] = (cx, cy)
                    objects_bbs_ids.append([x, y, w, h, object_id])
                    same_object_detected = True
                    break

            # se não encontrou nenhum ID próximo, cria um novo
            if not same_object_detected:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1

        # limpa IDs que não apareceram neste frame
        new_center_points = {}
        for x, y, w, h, object_id in objects_bbs_ids:
            cx = x + w // 2
            cy = y + h // 2
            new_center_points[object_id] = (cx, cy)

        self.center_points = new_center_points.copy()

        return objects_bbs_ids
